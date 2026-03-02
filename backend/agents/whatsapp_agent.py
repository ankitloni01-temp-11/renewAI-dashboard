"""WhatsApp Execution Agent using MCP."""
import json, time, uuid, asyncio
from typing import Dict, Any
from mcp_client.client import mcp

async def run_whatsapp_agent(policy_id: str, plan: Dict, orchestrator_result: Dict) -> Dict[str, Any]:
    start = time.time()
    # Mock generation
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    message = f"Hi {customer.get('name')}, your policy {policy_id} is due for renewal. Tap here to pay: https://pay.suraksha.in/w/{policy_id}"
    
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 4, "agent_name": "WhatsAppAgent",
            "action": "generate_whatsapp",
            "input_summary": f"Generating WhatsApp for {policy_id}",
            "output_summary": "WhatsApp message ready",
            "verdict": "GENERATED", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    })
    return {"body_text": message, "status": "ready"}
