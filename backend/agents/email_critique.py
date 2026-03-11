import json, time, uuid, asyncio
from typing import Dict, Any
from mcp_client.client import mcp
from agents.gemini_caller import call_gemini
import prompts.all_prompts as ap

async def run_email_critique(policy_id: str, email_result: Dict, policy_data: Dict, customer_data: Dict) -> Dict[str, Any]:
    start = time.time()
    
    compliance_rules = await mcp.call_tool("knowledge", "get_compliance_rules", {})
    
    user_prompt = ap.EMAIL_CRITIQUE_USER_TEMPLATE.format(
        content_to_evaluate=json.dumps(email_result, indent=2),
        original_plan="Email outreach for renewal",
        customer_json=json.dumps(customer_data, indent=2),
        policy_json=json.dumps(policy_data, indent=2),
        compliance_rules=json.dumps(compliance_rules)
    )
    
    result_call = await call_gemini(ap.EMAIL_CRITIQUE_SYSTEM_PROMPT, user_prompt, use_pro=True)
    result = result_call.get("data", {}) if result_call["success"] else {}
    
    score = result.get("overall_score", 0)
    verdict = result.get("verdict", "REJECTED")
    feedback = result.get("specific_feedback", "Check content for compliance.")
    
    latency_ms = int((time.time() - start) * 1000)
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 5, "agent_name": "EmailCritique",
            "action": "critique_email",
            "input_summary": f"Critiquing {email_result.get('language')} email",
            "output_summary": f"Score: {score} | Verdict: {verdict}",
            "verdict": verdict, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "full_output": result,
            "latency_ms": latency_ms
        }
    })
    return {"score": score, "verdict": verdict, "feedback": feedback}
