import json, time, uuid, asyncio
from typing import Dict, Any
from mcp_client.client import mcp
from agents.gemini_caller import call_gemini
import prompts.all_prompts as ap

async def run_planner_critique(policy_id: str, plan: Dict, orch_result: Dict) -> Dict[str, Any]:
    start = time.time()
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    compliance_rules = await mcp.call_tool("knowledge", "get_compliance_rules", {})
    
    user_prompt = ap.CRITIQUE_USER_TEMPLATE.format(
        content_to_evaluate=json.dumps(plan, indent=2),
        original_plan=" стратегическое решение Orchestrator: " + json.dumps(orch_result, indent=2),
        customer_json=json.dumps(customer, indent=2),
        policy_json=json.dumps(policy, indent=2),
        compliance_rules=json.dumps(compliance_rules)
    )
    
    result_call = await call_gemini(ap.CRITIQUE_SYSTEM_PROMPT, user_prompt, use_pro=True)
    result = result_call.get("data", {}) if result_call["success"] else {}
    
    score = result.get("overall_score", 0)
    verdict = result.get("verdict", "REJECTED")
    feedback = result.get("specific_feedback", "No feedback provided.")
    
    latency_ms = int((time.time() - start) * 1000)
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 3, "agent_name": "PlannerCritique",
            "action": "critique_plan",
            "input_summary": f"Critiquing plan for {policy_id}",
            "output_summary": f"Score: {score} | Verdict: {verdict}",
            "verdict": verdict, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "full_output": result,
            "latency_ms": latency_ms
        }
    })
    return {"score": score, "verdict": verdict, "feedback": feedback}
