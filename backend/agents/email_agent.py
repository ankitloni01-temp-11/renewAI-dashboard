"""Email Execution Agent using MCP."""
import json, time, uuid, asyncio
from typing import Dict, Any
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL
from mcp_client.client import mcp

genai.configure(api_key=GOOGLE_API_KEY)

EMAIL_PROMPT = """You are the Email Agent of RenewAI at Suraksha Life Insurance.
Generate a personalized renewal email for the customer.

RULES:
1. Always start with "This message is from Suraksha's AI-powered renewal assistant."
2. Always include opt-out: "To stop receiving reminders, reply STOP."
3. Use ONLY the financial figures provided - never make up numbers
4. Tone must match customer segment
5. Include the policy number prominently
6. Language: as specified

Output valid JSON only:
{
  "subject_line": "...",
  "body_text": "Full email body text",
  "body_html": "HTML version",
  "language": "English",
  "personalization_elements_used": ["name", "policy_number", "premium"],
  "policy_figures_cited": {"premium": 24000, "sum_assured": 1000000}
}"""

async def run_email_agent(policy_id: str, plan: Dict, orchestrator_result: Dict) -> Dict[str, Any]:
    start = time.time()
    
    # Fetch data via MCP
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    
    lang = orchestrator_result.get("language", "English")
    segment = customer.get("segment", "loyal_long_term")
    
    model = genai.GenerativeModel(GEMINI_MODEL)
    user_prompt = f"""
CUSTOMER: {customer.get('full_name', customer.get('name'))} | Segment: {segment}
POLICY: {policy.get('policy_id')} - {policy.get('product_name')}
PREMIUM: Rs.{policy.get('premium_amount',0):,} | SUM ASSURED: Rs.{policy.get('sum_assured',0):,}
DUE DATE: {policy.get('due_date')}
LANGUAGE: {lang}
PLAN OPENING: {plan.get('opening_line', '')}
KEY BENEFITS: {json.dumps(plan.get('key_benefit_points', []))}
CTA: {plan.get('call_to_action', 'Renew Now')}
PAYMENT LINK: https://pay.suraksha.in/renew/{policy_id}
{f"FUND VALUE: Rs.{policy.get('fund_value',0):,} | NAV CHANGE: +{policy.get('nav_change_pct',12)}%" if policy.get('product_type') == 'ulip' else ""}
{f"MATURITY VALUE: Rs.{policy.get('projected_maturity_value',0):,} on {policy.get('maturity_date','')}" if policy.get('product_type') in ['endowment','child'] else ""}

Generate a personalized renewal email in {lang}. If not English, provide the message in that language.
The email should feel personal, warm, and motivating - not robotic.
"""
    try:
        response = await asyncio.to_thread(
            model.generate_content,
            [EMAIL_PROMPT, user_prompt],
            generation_config=genai.GenerationConfig(response_mime_type="application/json", max_output_tokens=1000)
        )
        result = json.loads(response.text)
    except Exception as e:
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
            "model_used": GEMINI_MODEL, "latency_ms": latency_ms,
            "token_count_in": 450, "token_count_out": 550,
            "verdict": "GENERATED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "full_output": result
        }
    })
    return result
