import json, time, uuid, asyncio
from typing import Dict, Any
from agents.gemini_caller import call_gemini
import prompts.all_prompts as ap
from mcp_client.client import mcp
from config import GEMINI_MODEL

async def run_planner(policy_id: str, orchestrator_result: Dict, feedback: str = "") -> Dict[str, Any]:
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
    
    user_prompt = ap.PLANNER_USER_TEMPLATE.format(
        orchestrator_output=json.dumps(orchestrator_result, indent=2),
        customer_json=json.dumps(customer, indent=2),
        policy_json=json.dumps(policy, indent=2),
        rag_context="N/A", # Will add real RAG in Layer 3
        objection_context=json.dumps(relevant_objections),
        feedback=feedback or "None. This is the first attempt."
    )
    
    result_call = await call_gemini(ap.PLANNER_SYSTEM_PROMPT, user_prompt)
    result = result_call.get("data", {}) if result_call["success"] else None
    
    if not result:
        result = {
            "message_structure": ["greeting", "policy_reminder", "benefit_highlight", "payment_cta", "opt_out"],
            "key_benefit_points": benefits_map.get(product_type, benefits_map["term"]),
            "objection_responses_to_preload": [o.get("objection") for o in relevant_objections] if relevant_objections else ["payment_flexibility"],
            "send_timing": "7:30 PM" if customer.get("preferred_contact_time") == "evening" else "10:30 AM",
            "personalization_elements": ["customer_name", "policy_number", "premium_amount", "due_date"],
            "payment_options_to_offer": payment_options,
            "opening_line": f"Hi {customer.get('first_name', 'there')}, your {policy.get('product_name')} policy is up for renewal.",
            "call_to_action": "Tap here to renew now",
            "error": result_call.get("error", "Unknown error")
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
            "model_used": result_call.get("model", GEMINI_MODEL), "latency_ms": latency_ms,
            "token_count_in": result_call.get("token_count_in", 400), "token_count_out": result_call.get("token_count_out", 300),
            "verdict": "CREATED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "full_output": result
        }
    })
    return result
