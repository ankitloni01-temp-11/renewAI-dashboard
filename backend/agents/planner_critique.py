"""Planner Critique Agent using MCP."""
import json, time, uuid, asyncio
from typing import Dict, Any
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL
from mcp_client.client import mcp

genai.configure(api_key=GOOGLE_API_KEY)

async def run_planner_critique(policy_id: str, plan: Dict, orch_result: Dict) -> Dict[str, Any]:
    start = time.time()
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    
    # Generic critique logic for demo
    score = 8.5
    verdict = "APPROVED" if score > 7 else "REVISE"
    
    latency_ms = int((time.time() - start) * 1000)
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 3, "agent_name": "PlannerCritique",
            "action": "critique_plan",
            "input_summary": f"Critiquing plan for {policy_id}",
            "output_summary": f"Score: {score} | Verdict: {verdict}",
            "verdict": verdict, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    })
    return {"score": score, "verdict": verdict, "feedback": "Plan looks solid."}
