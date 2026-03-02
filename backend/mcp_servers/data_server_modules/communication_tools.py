"""Communication tool handlers with simulated background events."""
import uuid
import time
import asyncio
from typing import Dict, Any, List
from . import shared_state as state

def send_email(arguments: Dict) -> Dict:
    msg_id = f"MSG-{str(uuid.uuid4())[:8].upper()}"
    state.messages[msg_id] = {
        "id": msg_id,
        "channel": "email",
        "recipient": arguments.get("to"),
        "subject": arguments.get("subject"),
        "body": arguments.get("body"),
        "status": "sent",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    return {"status": "success", "message_id": msg_id}

def send_whatsapp(arguments: Dict) -> Dict:
    msg_id = f"MSG-{str(uuid.uuid4())[:8].upper()}"
    state.messages[msg_id] = {
        "id": msg_id,
        "channel": "whatsapp",
        "recipient": arguments.get("to"),
        "body": arguments.get("body"),
        "status": "delivered",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    return {"status": "success", "message_id": msg_id}

def initiate_voice_call(arguments: Dict) -> Dict:
    msg_id = f"MSG-{str(uuid.uuid4())[:8].upper()}"
    state.messages[msg_id] = {
        "id": msg_id,
        "channel": "voice",
        "recipient": arguments.get("to"),
        "status": "ringing",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    return {"status": "success", "message_id": msg_id}

def get_message_status(arguments: Dict) -> Dict:
    msg_id = arguments.get("message_id")
    return state.messages.get(msg_id, {"status": "not_found"})

def get_channel_stats(arguments: Dict) -> Dict:
    # Count messages per channel
    stats = {"email": 0, "whatsapp": 0, "voice": 0}
    for m in state.messages.values():
        c = m.get("channel")
        if c in stats:
            stats[c] += 1
    return stats
