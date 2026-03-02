"""LangGraph StateGraph using the MCP unified client."""
import asyncio, json, time, uuid
from typing import Dict, Any
from mcp_client.client import mcp
from agents.orchestrator import run_orchestrator
from agents.planner import run_planner
from agents.planner_critique import run_planner_critique
from agents.email_agent import run_email_agent
from agents.email_critique import run_email_critique
from datetime import datetime

async def _delay(seconds=1.0):
    await asyncio.sleep(seconds)

async def run_renewal_journey(policy_id: str) -> Dict[str, Any]:
    """Run the fully refactored MCP-based renewal journey."""
    
    # 1. Fetch data via MCP Data Server
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    if not policy:
        return {"error": f"Policy {policy_id} not found", "status": "error"}
    
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    
    # 2. Initialize journey via MCP Knowledge/Data Server
    journey = await mcp.call_tool("data", "get_journey_state", {"policy_id": policy_id})
    if not journey:
        journey = await mcp.call_tool("data", "create_journey", {"policy_id": policy_id})
    
    journey.update({
        "status": "planning",
        "current_step": "ORCHESTRATING",
        "started_at": datetime.now().isoformat()
    })
    await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": journey})
    
    try:
        # Step 1: Orchestrator
        await _delay(1)
        # Updates are handled internally or can be pushed via MCP
        orch_result = await run_orchestrator(policy_id)
        
        # Step 2: Planner
        await _delay(0.5)
        await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": {"current_step": "PLANNING"}})
        plan = await run_planner(policy_id, orch_result)
        
        # Step 3: Planner Critique (max 3 attempts) - Note: critiques should also be moved to MCP eventually
        for attempt in range(2):
            await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": {"current_step": f"CRITIQUE_ATTEMPT_{attempt+1}"}})
            critique = await run_planner_critique(policy_id, plan, orch_result)
            if critique.get("verdict") == "APPROVED":
                break
            await _delay(0.5)
        
        # Step 4: Execute via appropriate channel
        channel = orch_result.get("recommended_channel", customer.get("preferred_channel", "email"))
        await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": {"channel": channel, "language": orch_result.get("language", "English")}})
        
        if channel == "email":
            await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": {"current_step": "GENERATING_EMAIL"}})
            email_result = await run_email_agent(policy_id, plan, orch_result)
            
            # Email critique
            email_critique = await run_email_critique(policy_id, email_result, policy, customer)
            
            # Step 5: Safety gate via MCP Safety Server
            await _delay(0.5)
            await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": {"current_step": "SAFETY_SCAN"}})
            body_text = email_result.get("body_text", "")
            
            safety = await mcp.call_tool("safety", "full_safety_check", {"content": body_text})
            
            if not safety.get("approved") or safety.get("distress", {}).get("distress_detected"):
                reason = "distress_detected" if safety.get("distress", {}).get("distress_detected") else "compliance_shield"
                await mcp.call_tool("data", "escalate_to_human", {"policy_id": policy_id, "reason": reason})
                await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": {"status": "escalated", "current_step": "ESCALATED"}})
                return {"status": "escalated", "reason": reason}
            
            # Step 6: Mock delivery via MCP Data Communication tool
            await mcp.call_tool("data", "send_email", {
                "to": customer.get("email"),
                "subject": email_result.get("subject_line"),
                "body": safety.get("final_content")
            })
            
            await mcp.call_tool("data", "update_journey_state", {
                "policy_id": policy_id, 
                "updates": {"status": "email_sent", "current_step": "COMPLETED"}
            })
            
        elif channel in ["whatsapp", "voice"]:
            # WhatsApp/Voice prep
            await mcp.call_tool("data", f"send_{channel}" if channel == "whatsapp" else "initiate_voice_call", {
                "to": customer.get("phone"),
                "body": f"Renewal for {policy_id} is ready."
            })
            await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": {"status": f"{channel}_sent", "current_step": "COMPLETED"}})
        
        # 7. Final Completion Audit via MCP
        await mcp.call_tool("data", "write_audit_entry", {
            "entry": {
                "event_id": str(uuid.uuid4()), "policy_id": policy_id,
                "step_number": 10, "agent_name": "JourneyComplete",
                "action": "journey_completed",
                "input_summary": f"Journey for {policy_id}",
                "output_summary": f"Channel: {channel}, Status: COMPLETED",
                "verdict": "COMPLETED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        })
        
        return {"status": "success", "channel": channel}
        
    except Exception as e:
        await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": {"status": "error", "error": str(e)}})
        return {"status": "error", "error": str(e)}
