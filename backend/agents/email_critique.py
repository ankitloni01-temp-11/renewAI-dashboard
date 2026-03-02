"""Email Critique Agent using MCP."""
import json, time, uuid, asyncio
from typing import Dict, Any
from mcp_client.client import mcp

async def run_email_critique(policy_id: str, email_result: Dict, policy_data: Dict, customer_data: Dict) -> Dict[str, Any]:
    start = time.time()
    
    # Simple heuristic critique
    score = 9.0
    issues = []
    if len(email_result.get("body_text", "")) < 100:
        score -= 2
        issues.append("Email body too short")
        
    verdict = "APPROVED" if score >= 7 else "REVISE"
    
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 5, "agent_name": "EmailCritique",
            "action": "critique_email",
            "input_summary": f"Critiquing {email_result.get('language')} email",
            "output_summary": f"Score: {score} | Verdict: {verdict}",
            "verdict": verdict, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    })
    return {"score": score, "verdict": verdict, "issues": issues}
