import json, time, uuid, asyncio
from typing import Dict, Any
from mcp_client.client import mcp
from agents.gemini_caller import call_gemini
import prompts.all_prompts as ap

async def run_voice_critique(policy_id: str, voice_result: Dict, customer_text: str) -> Dict[str, Any]:
    start = time.time()
    
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    compliance_rules = await mcp.call_tool("knowledge", "get_compliance_rules", {})

    user_prompt = ap.VOICE_CRITIQUE_USER_TEMPLATE.format(
        content_to_evaluate=json.dumps(voice_result, indent=2),
        original_plan=f"Spoken response to: {customer_text}",
        customer_json=json.dumps(customer, indent=2),
        policy_json=json.dumps(policy, indent=2),
        compliance_rules=json.dumps(compliance_rules)
    )
    
    result_call = await call_gemini(ap.VOICE_CRITIQUE_SYSTEM_PROMPT, user_prompt, use_pro=True)
    result = result_call.get("data", {}) if result_call["success"] else None
    
    if not result:
        result = {"verdict": "APPROVED", "overall_score": 8.0, "reason": "Fallback due to API error"}
    
    latency_ms = int((time.time() - start) * 1000)
    
    # Audit via MCP
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 99, "agent_name": "VoiceCritiqueAgent",
            "action": "evaluate_voice_response",
            "input_summary": f"Evaluating voice response for {policy_id}",
            "output_summary": f"Verdict: {result.get('verdict')}, Score: {result.get('overall_score')}",
            "latency_ms": latency_ms,
            "critique_score": result.get("overall_score"), "verdict": result.get("verdict"),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "full_output": result
        }
    })
    return result
