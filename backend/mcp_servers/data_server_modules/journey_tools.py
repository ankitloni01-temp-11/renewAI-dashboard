"""Journey and Audit tool handlers."""
import uuid
import time
from typing import Dict, Any, List
from . import shared_state as state

def get_journey_state(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    return state.journeys.get(policy_id, {})

def create_journey(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    journey = {
        "journey_id": f"JRN-{str(uuid.uuid4())[:8].upper()}",
        "policy_id": policy_id,
        "status": "active",
        "current_step": "init",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    state.journeys[policy_id] = journey
    return journey

def update_journey_state(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    updates = arguments.get("updates", {})
    if policy_id in state.journeys:
        state.journeys[policy_id].update(updates)
        return state.journeys[policy_id]
    return {}

def write_audit_entry(arguments: Dict) -> Dict:
    entry = arguments.get("entry", {})
    if "timestamp" not in entry:
        entry["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    state.audit_trail.append(entry)
    return {"status": "success", "audit_id": entry.get("event_id")}

def get_audit_trail(arguments: Dict) -> List[Dict]:
    policy_id = arguments.get("policy_id")
    if policy_id:
        return [e for e in state.audit_trail if e.get("policy_id") == policy_id]
    return state.audit_trail

def append_conversation_message(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    message = arguments.get("message")
    if policy_id not in state.conversations:
        state.conversations[policy_id] = []
    state.conversations[policy_id].append(message)
    return {"status": "success"}

def get_conversation_history(arguments: Dict) -> List[Dict]:
    policy_id = arguments.get("policy_id")
    return state.conversations.get(policy_id, [])
