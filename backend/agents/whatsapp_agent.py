import json, time, uuid, asyncio
from typing import Dict, Any
from agents.gemini_caller import call_gemini
import prompts.all_prompts as ap
from mcp_client.client import mcp
from config import GEMINI_MODEL

async def run_whatsapp_agent(policy_id: str, plan: Dict, orchestrator_result: Dict, customer_message: str = "INITIAL_OUTREACH", history: list = None) -> Dict[str, Any]:
    start = time.time()
    
    # Fetch data via MCP
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    objection_results = await mcp.call_tool("knowledge", "search_objections", {"query": orchestrator_result.get('segment_approach', ''), "n": 3})
    
    user_prompt = ap.WHATSAPP_AGENT_USER_TEMPLATE.format(
        customer_name=customer.get('full_name', customer.get('name', 'valued customer')),
        language=orchestrator_result.get('language', 'English'),
        segment=customer.get('segment', 'loyal_long_term'),
        policy_id=policy_id,
        product_name=policy.get('product_name', 'policy'),
        premium=policy.get('premium_amount', 0),
        due_date=policy.get('due_date', ''),
        extra_fields="",
        conversation_history=json.dumps(history or []),
        customer_message=customer_message,
        objection_context=json.dumps(objection_results.get("results", []))
    )
    
    result_call = await call_gemini(ap.WHATSAPP_AGENT_SYSTEM_PROMPT, user_prompt)
    result = result_call.get("data", {}) if result_call["success"] else None
    
    if not result:
        result = {
            "response_text": f"Hi {customer.get('name')}, your policy {policy_id} is due for renewal. Tap here to pay: https://pay.suraksha.in/w/{policy_id}",
            "detected_intent": "greeting",
            "sentiment": "neutral",
            "emoji_used": ["📋"],
            "payment_link_included": True,
            "escalation_needed": False,
            "error": result_call.get("error", "Unknown error")
        }
    
    latency_ms = int((time.time() - start) * 1000)
    
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 4, "agent_name": "WhatsAppAgent",
            "action": "generate_whatsapp",
            "input_summary": f"Generating WhatsApp for {policy_id}",
            "output_summary": f"Intent: {result.get('detected_intent')}",
            "model_used": result_call.get("model", GEMINI_MODEL), "latency_ms": latency_ms,
            "token_count_in": result_call.get("token_count_in", 300), "token_count_out": result_call.get("token_count_out", 200),
            "verdict": "GENERATED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "full_output": result
        }
    })
    return result
