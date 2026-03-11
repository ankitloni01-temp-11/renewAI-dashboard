import json
import uuid
import asyncio
from datetime import datetime, date
from typing import Dict, Any
from agents.gemini_caller import call_gemini
import prompts.all_prompts as ap
from mcp_client.client import mcp


async def run_orchestrator(policy_id: str) -> Dict[str, Any]:
    """Run the Orchestrator Agent for a given policy using MCP tools."""
    
    # Fetch all context via MCP Data Server
    policy_data = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer_data = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    propensity_data = await mcp.call_tool("data", "get_propensity_score", {"policy_id": policy_id})
    conversation_history = await mcp.call_tool("data", "get_conversation_history", {"policy_id": policy_id})
    
    trace_id = str(uuid.uuid4())

    days_to_due = 45
    try:
        due_str = policy_data.get("due_date", "2026-03-15")
        due = datetime.strptime(due_str, "%Y-%m-%d")
        days_to_due = (due - datetime.now()).days
    except Exception:
        pass

    user_prompt = ap.ORCHESTRATOR_USER_TEMPLATE.format(
        current_date=date.today().isoformat(),
        days_to_due=days_to_due,
        customer_json=json.dumps(customer_data, ensure_ascii=False),
        policy_json=json.dumps(policy_data, ensure_ascii=False),
        propensity_json=json.dumps(propensity_data, ensure_ascii=False),
        conversation_history=json.dumps(conversation_history[-5:], ensure_ascii=False) if conversation_history else "[]"
    )

    result = await call_gemini(ap.ORCHESTRATOR_SYSTEM_PROMPT, user_prompt, use_pro=True)

    # Write audit event via MCP
    event = {
        "event_id": str(uuid.uuid4()),
        "trace_id": trace_id,
        "policy_id": policy_id,
        "step_number": 1,
        "agent_name": "Orchestrator",
        "action": "strategic_analysis",
        "input_summary": f"Analyzing renewal for {customer_data.get('name', 'Unknown')} | Days to due: {days_to_due}",
        "output_summary": (
            f"Channel: {result['data'].get('recommended_channel', 'unknown')} | "
            f"Risk: {result['data'].get('risk_assessment', 'unknown')}"
        ) if result["success"] else f"Error: {result.get('error', 'Unknown')}",
        "full_input": {"days_to_due": days_to_due},
        "full_output": result.get("data", {}),
        "model_used": result.get("model"),
        "latency_ms": result.get("latency_ms"),
        "token_count_in": result.get("token_count_in"),
        "token_count_out": result.get("token_count_out"),
        "critique_score": None,
        "verdict": "SUCCESS" if result["success"] else "ERROR",
        "timestamp": datetime.now().isoformat()
    }
    await mcp.call_tool("data", "write_audit_entry", {"entry": event})

    if not result["success"]:
        # Fallback decision
        return {
            "recommended_channel": customer_data.get("preferred_channel", "whatsapp"),
            "language": customer_data.get("preferred_language", "English"),
            "tone": "warm",
            "segment_approach": "Standard renewal approach",
            "preferred_send_time": customer_data.get("preferred_contact_time", "evening"),
            "risk_assessment": "MEDIUM",
            "special_flags": [],
            "escalate_to_human": False,
            "escalation_reason": None,
            "objective_for_planner": f"Send renewal reminder for {policy_data.get('product_name', 'policy')} due {due_str}",
            "key_value_propositions": ["Life cover continuation", "Family protection"],
            "payment_options_to_highlight": ["UPI", "Net Banking", "Credit Card"]
        }

    return result["data"]
