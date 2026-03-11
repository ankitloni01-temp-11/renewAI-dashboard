import json, time, uuid, asyncio
from typing import Dict, Any
from agents.gemini_caller import call_gemini
import prompts.all_prompts as ap
from mcp_client.client import mcp
from config import GEMINI_MODEL

async def run_email_agent(policy_id: str, plan: Dict, orchestrator_result: Dict) -> Dict[str, Any]:
    start = time.time()
    
    # Fetch data via MCP
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    
    lang = orchestrator_result.get("language", "English")
    segment = customer.get("segment", "loyal_long_term")
    
    user_prompt = ap.EMAIL_AGENT_USER_TEMPLATE.format(
        execution_plan=json.dumps(plan, indent=2),
        customer_name=customer.get('full_name', customer.get('name', 'valued customer')),
        language=lang,
        segment=segment,
        tenure=customer.get('tenure_years', 0),
        policy_id=policy_id,
        product_name=policy.get('product_name', 'policy'),
        premium=policy.get('premium_amount', 0),
        sum_assured=policy.get('sum_assured', 0),
        due_date=policy.get('due_date', ''),
        extra_policy_fields=f"Due Date: {policy.get('due_date')}", # Simple inclusion
        rag_context="N/A"
    )
    
    result_call = await call_gemini(ap.EMAIL_AGENT_SYSTEM_PROMPT, user_prompt)
    result = result_call.get("data", {}) if result_call["success"] else None
    
    if not result:
        result = {
            "subject_line": f"Important: Your {policy.get('product_name')} Policy Renewal Due {policy.get('due_date')}",
            "body_text": f"""This message is from Suraksha's AI-powered renewal assistant.\n\nDear {customer.get('first_name', 'Valued Customer')},\n\nYour {policy.get('product_name')} (Policy No: {policy_id}) is due for renewal on {policy.get('due_date')}.\n\nPremium Amount: Rs.{policy.get('premium_amount',0):,}\nLife Cover: Rs.{policy.get('sum_assured',0):,}\n\nRenew now: https://pay.suraksha.in/renew/{policy_id}\n\nThank you for trusting Suraksha for your family's protection.\n\nTo stop receiving reminders, reply STOP.""",
            "body_html": f"<p>Dear {customer.get('first_name')},</p><p>Your policy is due for renewal.</p>",
            "language": lang,
            "personalization_elements_used": ["name", "policy_number", "premium", "due_date"],
            "policy_figures_cited": {"premium": policy.get('premium_amount'), "sum_assured": policy.get('sum_assured')}
        }
    
    latency_ms = int((time.time() - start) * 1000)
    
    # Audit via MCP
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), 
            "policy_id": policy_id,
            "step_number": 4, "agent_name": "EmailAgent",
            "action": "generate_email",
            "input_summary": f"Generating {lang} email via MCP",
            "output_summary": f"Subject: {result.get('subject_line','')[:50]}",
            "model_used": result_call.get("model", GEMINI_MODEL), "latency_ms": latency_ms,
            "token_count_in": result_call.get("token_count_in", 450), "token_count_out": result_call.get("token_count_out", 550),
            "verdict": "GENERATED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "full_output": result
        }
    })
    return result
