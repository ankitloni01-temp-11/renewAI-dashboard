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
    
    # Fetch journey state for plan/orch results
    journey = await mcp.call_tool("data", "get_journey_state", {"policy_id": policy_id})
    if not journey:
        plan = {"message_structure": ["greeting"]}
        orch_result = {"language": "English", "segment_approach": "retention"}
    else:
        plan = journey.get("full_output", {}).get("plan", {"message_structure": ["greeting"]})
        orch_result = journey.get("full_output", {}).get("orchestrator_result", {"language": "English", "segment_approach": "retention"})

    # Run agent
    wa_result = await run_whatsapp_agent(policy_id, plan, orch_result, customer_message, history)
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

@router.post("/voice/turn")
async def voice_turn(policy_id: str, call_id: str, customer_text: str):
    """Handle a single turn in a voice conversation."""
    # 1. Get journey state to access the plan and orchestrator result
    journey = await mcp.call_tool("data", "get_journey_state", {"policy_id": policy_id})
    if not journey:
        # Fallback for demo if journey not started
        plan = {"message_structure": ["greeting", "objection_handling", "cta"]}
        orch_result = {"language": "Hindi", "tone": "warm", "segment_approach": "retention"}
    else:
        # In a real system, we'd pull the latest plan and orch result from the journey data
        # For the demo, we use stored results or defaults
        plan = journey.get("full_output", {}).get("plan", {"message_structure": ["greeting"]})
        orch_result = journey.get("full_output", {}).get("orchestrator_result", {"language": "English"})

    # 2. Get history
    history = await mcp.call_tool("data", "get_conversation_history", {"policy_id": policy_id})

    # 3. Run Voice Agent
    voice_result = await run_voice_agent(policy_id, plan, orch_result, customer_text, history)
    
    # 4. Run Voice Critique
    critique = await run_voice_critique(policy_id, voice_result, customer_text)
    
    # 4. Append to history via MCP
    timestamp = datetime.now().isoformat()
    await mcp.call_tool("data", "append_conversation_message", {
        "policy_id": policy_id,
        "message": {
            "message_id": str(uuid.uuid4()),
            "role": "customer",
            "customer_text": customer_text,
            "timestamp": timestamp,
            "channel": "voice",
            "call_id": call_id
        }
    })
    
    ai_msg = {
        "message_id": str(uuid.uuid4()),
        "role": "ai",
        "ai_response": voice_result.get("response_text", ""),
        "detected_intent": voice_result.get("detected_intent"),
        "critique_score": critique.get("overall_score"),
        "timestamp": timestamp,
        "channel": "voice",
        "call_id": call_id
    }
    await mcp.call_tool("data", "append_conversation_message", {"policy_id": policy_id, "message": ai_msg})
    
    return {
        "ai_response": voice_result.get("response_text"),
        "detected_intent": voice_result.get("detected_intent"),
        "critique_score": critique.get("overall_score"),
        "escalated": voice_result.get("escalation_needed", False),
        "case_id": f"CS-{uuid.uuid4().hex[:6].upper()}" if voice_result.get("escalation_needed") else None
    }

@router.get("/{policy_id}/history")
async def get_conversation_history(policy_id: str):
    history = await mcp.call_tool("data", "get_conversation_history", {"policy_id": policy_id})
    return {
        "policy_id": policy_id,
        "history": history,
        "total_messages": len(history)
    }
