"""Human Queue Manager Agent using MCP."""
import json, time, uuid, asyncio
from typing import Dict, Any, List
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL
from mcp_client.client import mcp
from datetime import datetime

genai.configure(api_key=GOOGLE_API_KEY)

HQ_PROMPT = """You are the Human Queue Manager of RenewAI at Suraksha Life Insurance.
A case has been escalated to a human specialist. Generate a comprehensive briefing note.

Include:
1. Situation summary (2-3 sentences)
2. Recommended approach (specific, actionable)
3. Priority level: URGENT or STANDARD
4. Specialist type: senior_rrm, revival_specialist, or compliance_handler
5. Recommended resolution options (list 3-4 specific options)

JSON only."""

async def create_queue_case(policy_id: str, escalation_reason: str, conversation_history: List[Dict], triggering_message: str = "") -> Dict[str, Any]:
    start = time.time()
    
    # Fetch data via MCP
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    propensity = await mcp.call_tool("data", "get_propensity_score", {"policy_id": policy_id})
    
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    user_prompt = f"""
ESCALATION REASON: {escalation_reason}
TRIGGERING MESSAGE: "{triggering_message}"
CUSTOMER: {customer.get('full_name')} | Segment: {customer.get('segment')}
POLICY: {policy_id} - {policy.get('product_name')}
"""
    
    try:
        response = await asyncio.to_thread(
            model.generate_content,
            [HQ_PROMPT, user_prompt],
            generation_config=genai.GenerationConfig(response_mime_type="application/json", max_output_tokens=600)
        )
        result = json.loads(response.text)
    except Exception:
        result = {
            "briefing_note": f"Escalation for {policy_id}",
            "recommended_approach": "Manual intervention required.",
            "priority_level": "STANDARD",
            "assigned_specialist_type": "senior_rrm"
        }
    
    # Create queue case via MCP Data Server
    case_id = f"CASE-{str(uuid.uuid4())[:8].upper()}"
    queue_case = {
        "case_id": case_id,
        "policy_id": policy_id,
        "customer_name": customer.get("full_name", customer.get("name")),
        "priority": result.get("priority_level", "STANDARD"),
        "reason": escalation_reason,
        "escalated_at": datetime.now().isoformat(),
        "status": "unassigned",
        "briefing_note": result.get("briefing_note"),
        "recommended_approach": result.get("recommended_approach"),
        "assigned_specialist_type": result.get("assigned_specialist_type"),
        "conversation_history": conversation_history
    }
    
    await mcp.call_tool("data", "escalate_to_human", {"policy_id": policy_id, "reason": escalation_reason})
    
    # Audit via MCP
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 99, "agent_name": "HumanQueueManager",
            "action": "create_queue_case",
            "input_summary": f"Escalation: {escalation_reason}",
            "output_summary": f"Case {case_id} created",
            "verdict": "ESCALATED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    })
    return queue_case
