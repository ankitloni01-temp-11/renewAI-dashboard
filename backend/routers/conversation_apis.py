"""WhatsApp + Voice conversation endpoints using MCP."""
from fastapi import APIRouter
from typing import Optional, List, Dict
from mcp_client.client import mcp
from agents.whatsapp_agent import run_whatsapp_agent
from agents.whatsapp_critique import run_whatsapp_critique
from agents.voice_agent import run_voice_agent
from agents.voice_critique import run_voice_critique
from agents.human_queue_manager import create_queue_case
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

@router.post("/whatsapp/message")
async def whatsapp_message(policy_id: str, customer_message: str):
    """Send a WhatsApp message via AI and store in MCP Data Server."""
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    if not policy:
        return {"error": "Policy not found"}
    
    history = await mcp.call_tool("data", "get_conversation_history", {"policy_id": policy_id})
    
    # Agents now use MCP internally for their auditing
    wa_result = await run_whatsapp_agent(policy_id, customer_message, history)
    critique = await run_whatsapp_critique(policy_id, wa_result, customer_message)
    
    timestamp = datetime.now().isoformat()
    # Store messages via MCP
    await mcp.call_tool("data", "append_conversation_message", {
        "policy_id": policy_id,
        "message": {
            "message_id": str(uuid.uuid4()),
            "role": "customer",
            "customer_text": customer_message,
            "timestamp": timestamp,
            "channel": "whatsapp"
        }
    })
    
    ai_msg = {
        "message_id": str(uuid.uuid4()),
        "role": "ai",
        "ai_response": wa_result.get("response_text", ""),
        "detected_intent": wa_result.get("detected_intent"),
        "critique_score": critique.get("overall_score"),
        "safety_verdict": wa_result.get("safety_result", {}).get("verdict", "PASS"),
        "timestamp": timestamp,
        "channel": "whatsapp"
    }
    await mcp.call_tool("data", "append_conversation_message", {"policy_id": policy_id, "message": ai_msg})
    
    return {
        "ai_response": wa_result.get("response_text"),
        "detected_intent": wa_result.get("detected_intent"),
        "escalated": wa_result.get("escalation_needed", False),
        "conversation_history": (await mcp.call_tool("data", "get_conversation_history", {"policy_id": policy_id}))[-5:]
    }

@router.get("/{policy_id}/history")
async def get_conversation_history(policy_id: str):
    history = await mcp.call_tool("data", "get_conversation_history", {"policy_id": policy_id})
    return {
        "policy_id": policy_id,
        "history": history,
        "total_messages": len(history)
    }
