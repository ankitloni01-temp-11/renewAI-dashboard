"""Voice Execution Agent using MCP."""
import json, time, uuid, asyncio
from typing import Dict, Any
from mcp_client.client import mcp

async def run_voice_agent(policy_id: str, plan: Dict, orchestrator_result: Dict) -> Dict[str, Any]:
    start = time.time()
    # Mock generation
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    script = f"Hello {customer.get('name')}, calling from Suraksha Life regarding your renewal..."
    
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 4, "agent_name": "VoiceAgent",
            "action": "generate_script",
            "input_summary": f"Generating Voice script for {policy_id}",
            "output_summary": "Script ready",
            "verdict": "GENERATED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    })
    return {"script": script, "status": "ready"}
