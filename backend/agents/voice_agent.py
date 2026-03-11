import json, time, uuid, asyncio
from typing import Dict, Any, List
from agents.gemini_caller import call_gemini
import prompts.all_prompts as ap
from mcp_client.client import mcp
from config import GEMINI_MODEL

async def run_voice_agent(policy_id: str, plan: Dict, orchestrator_result: Dict, customer_text: str = "HELLO", history: List = None) -> Dict[str, Any]:
    start = time.time()
    
    # Fetch data via MCP
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    
    # RAG lookup for objections
    objection_query = f"{orchestrator_result.get('segment_approach', '')} {policy.get('product_type', '')} {customer_text}"
    objection_results = await mcp.call_tool("knowledge", "search_objections", {"query": objection_query, "n": 3})
    
    user_prompt = ap.VOICE_AGENT_USER_TEMPLATE.format(
        customer_name=customer.get('full_name', customer.get('name', 'valued customer')),
        language=orchestrator_result.get('language', 'English'),
        segment=customer.get('segment', 'loyal_long_term'),
        contact_time=customer.get('preferred_contact_time', 'evening'),
        policy_id=policy_id,
        product_name=policy.get('product_name', 'policy'),
        premium=policy.get('premium_amount', 0),
        due_date=policy.get('due_date', ''),
        extra_fields="",
        payment_status="DUE",
        objections_handled_count=len([m for m in (history or []) if m.get('detected_intent') == 'objection']),
        conversation_history=json.dumps(history or []),
        customer_text=customer_text,
        objection_context=json.dumps(objection_results.get("results", []))
    )
    
    result_call = await call_gemini(ap.VOICE_AGENT_SYSTEM_PROMPT, user_prompt)
    result = result_call.get("data", {}) if result_call["success"] else None
    
    if not result:
        result = {
            "response_text": f"Hello {customer.get('name')}, calling from Suraksha Life regarding your renewal.",
            "detected_intent": "greeting",
            "objection_handled": None,
            "payment_offered": False,
            "escalation_needed": False,
            "call_outcome_status": "in_progress",
            "error": result_call.get("error", "Unknown error")
        }
    
    latency_ms = int((time.time() - start) * 1000)
    
    # Audit via MCP
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 4, "agent_name": "VoiceAgent",
            "action": "generate_script",
            "input_summary": f"Generating Voice script for {policy_id}",
            "output_summary": f"Intent: {result.get('detected_intent')}",
            "model_used": result_call.get("model", GEMINI_MODEL), "latency_ms": latency_ms,
            "token_count_in": result_call.get("token_count_in", 300), "token_count_out": result_call.get("token_count_out", 200),
            "verdict": "GENERATED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "full_output": result
        }
    })
    return result
