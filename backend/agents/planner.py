"""Planner Agent using MCP for detailed execution plan."""
import json, time, uuid
from typing import Dict, Any
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL
from mcp_client.client import mcp

genai.configure(api_key=GOOGLE_API_KEY)

PLANNER_PROMPT = """You are the Planner Agent of RenewAI at Suraksha Life Insurance.
Your job is to create a detailed, personalized communication execution plan for a policy renewal.

Given the orchestrator's strategy and customer/policy data, create a specific execution plan.
Use the provided policy context and objection information to personalize the plan.

The plan must include:
- message_structure: how to structure the message (greeting, main message, CTA, closing)
- key_benefit_points: 2-3 specific benefits to highlight based on product type
- objection_responses_to_preload: top 3 likely objections for this customer
- send_timing: specific time to send (e.g., "7:30 PM" based on preferred contact time)
- personalization_elements: what personal details to include
- payment_options_to_offer: relevant payment options
- opening_line: the exact opening line to use
- call_to_action: the specific CTA text

Respond ONLY with valid JSON."""

async def run_planner(policy_id: str, orchestrator_result: Dict) -> Dict[str, Any]:
    start = time.time()
    
    # Fetch data via MCP
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    
    # RAG lookup for objections via MCP Knowledge Server
    objection_query = f"{orchestrator_result.get('segment_approach')} {policy.get('product_type')}"
    objection_results = await mcp.call_tool("knowledge", "search_objections", {"query": objection_query, "n": 3})
    relevant_objections = objection_results.get("results", [])
    
    product_type = policy.get("product_type", "term")
    segment = customer.get("segment", "loyal_long_term")
    
    benefits_map = {
        "term": ["life cover protection", "Section 80C tax benefit", "affordable premium for high cover"],
        "endowment": ["life cover + savings", "guaranteed maturity benefit", "annual bonus additions"],
        "ulip": [f"fund growth {policy.get('nav_change_pct', 12)}% this year", "flexible fund switching", "life cover + investment"],
        "pension": ["retirement income security", "tax-free corpus", "guaranteed pension from retirement age"],
        "child": ["child's education secured", "waiver of premium on parent's death", "guaranteed sum at child's 18th birthday"]
    }
    
    payment_options = ["UPI payment link", "Net banking", "Credit/Debit card"]
    if customer.get("segment") == "budget_conscious":
        payment_options = ["Monthly EMI (2% loading)", "Quarterly instalments", "UPI AutoPay setup"]
    
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    user_prompt = f"""
ORCHESTRATOR STRATEGY:
{json.dumps(orchestrator_result, indent=2)}

POLICY: {policy.get('product_name')} | Premium: Rs.{policy.get('premium_amount',0):,} | Due: {policy.get('due_date')}
CUSTOMER: {customer.get('full_name', customer.get('name'))} | Segment: {segment} | Tenure: {customer.get('tenure_years')} years | Language: {orchestrator_result.get('language')}
RELEVANT OBJECTIONS: {json.dumps(relevant_objections)}
PRODUCT BENEFITS: {json.dumps(benefits_map.get(product_type, benefits_map['term']))}
PAYMENT OPTIONS: {json.dumps(payment_options)}

Create a detailed execution plan. Use the customer's name "{customer.get('full_name', customer.get('name', 'valued customer'))}" in the opening.
"""
    
    try:
        response = await asyncio.to_thread(
            model.generate_content,
            [PLANNER_PROMPT, user_prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                max_output_tokens=600
            )
        )
        result = json.loads(response.text)
    except Exception as e:
        result = {
            "message_structure": ["greeting", "policy_reminder", "benefit_highlight", "payment_cta", "opt_out"],
            "key_benefit_points": benefits_map.get(product_type, benefits_map["term"]),
            "objection_responses_to_preload": [o.get("objection_text") for o in relevant_objections] if relevant_objections else ["payment_flexibility"],
            "send_timing": "7:30 PM" if customer.get("preferred_contact_time") == "evening" else "10:30 AM",
            "personalization_elements": ["customer_name", "policy_number", "premium_amount", "due_date"],
            "payment_options_to_offer": payment_options,
            "opening_line": f"Hi {customer.get('first_name', 'there')}, your {policy.get('product_name')} policy is up for renewal.",
            "call_to_action": "Tap here to renew now",
            "error": str(e)
        }
    
    latency_ms = int((time.time() - start) * 1000)
    
    # Audit via MCP
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()),
            "policy_id": policy_id,
            "step_number": 2, "agent_name": "PlannerAgent",
            "action": "create_execution_plan",
            "input_summary": f"Plan created via MCP Knowledge Server",
            "output_summary": f"Plan created with {len(result.get('key_benefit_points',[]))} benefits",
            "model_used": GEMINI_MODEL, "latency_ms": latency_ms,
            "token_count_in": 400, "token_count_out": 300,
            "verdict": "CREATED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "full_output": result
        }
    })
    return result
import asyncio
