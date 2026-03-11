"""RenewAI Journey LangGraph StateMachine."""
import asyncio
import json
import time
import uuid
from typing import Dict, Any, List, TypedDict, Annotated, Optional
import operator

from langgraph.graph import StateGraph, END
from mcp_client.client import mcp

from agents.orchestrator import run_orchestrator
from agents.planner import run_planner
from agents.planner_critique import run_planner_critique
from agents.email_agent import run_email_agent
from agents.email_critique import run_email_critique
from agents.whatsapp_agent import run_whatsapp_agent
from agents.whatsapp_critique import run_whatsapp_critique
from agents.voice_agent import run_voice_agent
from agents.voice_critique import run_voice_critique
from agents.content_safety import run_safety_check

# Define the state schema
class AgentState(TypedDict):
    policy_id: str
    customer: Dict[str, Any]
    policy: Dict[str, Any]
    orchestrator_result: Dict[str, Any]
    plan: Dict[str, Any]
    critique_feedback: str
    planner_attempts: int
    execution_result: Dict[str, Any]
    channel: str
    status: str
    current_step: str
    error: Optional[str]
    messages: List[Dict[str, Any]]

# --- NODES ---

async def node_orchestrate(state: AgentState):
    """Run the Orchestrator to decide strategy."""
    policy_id = state['policy_id']
    await mcp.call_tool("data", "update_journey_state", {
        "policy_id": policy_id, 
        "updates": {"current_step": "ORCHESTRATING", "status": "running"}
    })
    
    orch_result = await run_orchestrator(policy_id)
    
    # Fetch core data if not present
    policy = state.get('policy') or await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = state.get('customer') or await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    
    return {
        "orchestrator_result": orch_result,
        "policy": policy,
        "customer": customer,
        "channel": orch_result.get("recommended_channel", "email"),
        "current_step": "PLANNING"
    }

async def node_plan(state: AgentState):
    """Run the Planner to create execution steps."""
    policy_id = state['policy_id']
    orch_result = state['orchestrator_result']
    feedback = state.get('critique_feedback', "")
    attempts = state.get('planner_attempts', 0) + 1
    
    await mcp.call_tool("data", "update_journey_state", {
        "policy_id": policy_id, 
        "updates": {"current_step": f"PLANNING_ATTEMPT_{attempts}"}
    })
    
    plan = await run_planner(policy_id, orch_result, feedback=feedback)
    
    return {
        "plan": plan,
        "planner_attempts": attempts,
        "current_step": "CRITIQUING_PLAN"
    }

async def node_critique_plan(state: AgentState):
    """Evaluate the plan for quality and compliance."""
    policy_id = state['policy_id']
    plan = state['plan']
    orch_result = state['orchestrator_result']
    
    critique = await run_planner_critique(policy_id, plan, orch_result)
    
    if critique.get("verdict") == "APPROVED":
        return {"current_step": "EXECUTING", "critique_feedback": ""}
    else:
        return {
            "current_step": "REVISING_PLAN", 
            "critique_feedback": critique.get("feedback", "Plan rejected.")
        }

async def node_execute(state: AgentState):
    """Send message via recommended channel."""
    policy_id = state['policy_id']
    channel = state['channel']
    plan = state['plan']
    orch_result = state['orchestrator_result']
    
    await mcp.call_tool("data", "update_journey_state", {
        "policy_id": policy_id, 
        "updates": {"current_step": f"EXECUTING_{channel.upper()}"}
    })
    
    if channel == "email":
        result = await run_email_agent(policy_id, plan, orch_result)
    elif channel == "whatsapp":
        result = await run_whatsapp_agent(policy_id, plan, orch_result)
    elif channel == "voice":
        result = await run_voice_agent(policy_id, plan, orch_result)
    else:
        result = {"error": f"Unsupported channel: {channel}"}
        
    return {"execution_result": result, "current_step": "SAFETY_CHECK"}

async def node_safety(state: AgentState):
    """Final safety scan before delivery."""
    policy_id = state['policy_id']
    exec_result = state['execution_result']
    channel = state['channel']
    
    content = ""
    if channel == "email":
        content = exec_result.get("body_text", "")
    elif channel == "whatsapp":
        content = exec_result.get("response_text", "")
    elif channel == "voice":
        content = exec_result.get("response_text", "")
        
    safety = await run_safety_check(content, channel=channel)
    
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 6, "agent_name": "ContentSafetyGuard",
            "action": "safety_scan",
            "input_summary": f"Scanning {channel} content",
            "output_summary": f"Verdict: {safety.get('verdict')}",
            "verdict": safety.get("verdict"), "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "full_output": safety
        }
    })
    

    if safety.get("verdict") == "PASS":
        # Mock actual delivery
        customer = state['customer']
        if channel == "email":
            await mcp.call_tool("data", "send_email", {
                "to": customer.get("email"),
                "subject": exec_result.get("subject_line"),
                "body": safety.get("final_content")
            })
        elif channel in ["whatsapp", "voice"]:
            await mcp.call_tool("data", f"send_{channel}", {
                "to": customer.get("phone"),
                "body": safety.get("final_content")
            })
            
        return {"status": "completed", "current_step": "COMPLETED"}
    else:
        return {"status": "escalated", "current_step": "ESCALATED", "error": safety.get("reason")}

async def node_escalate(state: AgentState):
    """Handle failures or distress by escalating to human."""
    policy_id = state['policy_id']
    reason = state.get('error', "Critique failure")
    
    await mcp.call_tool("data", "escalate_to_human", {"policy_id": policy_id, "reason": reason})
    await mcp.call_tool("data", "update_journey_state", {
        "policy_id": policy_id, 
        "updates": {"status": "escalated", "current_step": "ESCALATED"}
    })
    return {"status": "escalated"}

# --- EDGES / ROUTING ---

def route_after_critique(state: AgentState):
    if state['current_step'] == "EXECUTING":
        return "trigger_execution"
    if state['planner_attempts'] >= 3:
        return "trigger_escalation"
    return "trigger_planning"

def route_after_safety(state: AgentState):
    if state['status'] == "completed":
        return "end"
    return "trigger_escalation"

# --- GRAPH DEFINITION ---

workflow = StateGraph(AgentState)

workflow.add_node("decide_strategy", node_orchestrate)
workflow.add_node("generate_plan", node_plan)
workflow.add_node("evaluate_plan", node_critique_plan)
workflow.add_node("execute_channel", node_execute)
workflow.add_node("verify_safety", node_safety)
workflow.add_node("handle_escalation", node_escalate)

workflow.set_entry_point("decide_strategy")

workflow.add_edge("decide_strategy", "generate_plan")
workflow.add_edge("generate_plan", "evaluate_plan")
workflow.add_conditional_edges(
    "evaluate_plan",
    route_after_critique,
    {
        "trigger_execution": "execute_channel",
        "trigger_planning": "generate_plan",
        "trigger_escalation": "handle_escalation"
    }
)
workflow.add_edge("execute_channel", "verify_safety")
workflow.add_conditional_edges(
    "verify_safety",
    route_after_safety,
    {
        "end": END,
        "trigger_escalation": "handle_escalation"
    }
)
workflow.add_edge("handle_escalation", END)

# Compile
app = workflow.compile()

async def run_renewal_journey(policy_id: str) -> Dict[str, Any]:
    """Entry point for the state machine."""
    initial_state = {
        "policy_id": policy_id,
        "planner_attempts": 0,
        "status": "starting",
        "current_step": "START",
        "messages": []
    }
    
    try:
        final_state = await app.ainvoke(initial_state)
        return {
            "status": final_state.get("status"),
            "channel": final_state.get("channel"),
            "current_step": final_state.get("current_step")
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            await mcp.call_tool("data", "update_journey_state", {
                "policy_id": policy_id, 
                "updates": {"status": "error", "error": str(e)}
            })
        except:
            pass
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # Test run
    async def test():
        print("Starting test...")
        try:
            # Increased timeout to 120s to allow for slow embeddings/pro models
            res = await asyncio.wait_for(run_renewal_journey("SLI-2298741"), timeout=120)
            print("Test result:")
            print(json.dumps(res, indent=2))
        except asyncio.TimeoutError:
            print("Test timed out after 120 seconds")
        except Exception as e:
            print(f"Test failed: {e}")
            import traceback
            traceback.print_exc()
            
    asyncio.run(test())
