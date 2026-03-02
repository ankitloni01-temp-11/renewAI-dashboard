"""Team and Human Queue tool handlers."""
import uuid
import time
from typing import Dict, Any, List
from . import shared_state as state

def escalate_to_human(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    reason = arguments.get("reason")
    case_id = f"CASE-{str(uuid.uuid4())[:8].upper()}"
    state.human_queue[policy_id] = {
        "case_id": case_id,
        "policy_id": policy_id,
        "reason": reason,
        "status": "pending",
        "escalated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    return {"status": "success", "case_id": case_id}

def get_queue(arguments: Dict) -> List[Dict]:
    return list(state.human_queue.values())

def assign_case(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    member_id = arguments.get("member_id")
    if policy_id in state.human_queue:
        state.human_queue[policy_id]["assigned_to"] = member_id
        state.human_queue[policy_id]["status"] = "assigned"
        return {"status": "success"}
    return {"status": "error"}

def update_case_status(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    status = arguments.get("status")
    if policy_id in state.human_queue:
        state.human_queue[policy_id]["status"] = status
        return {"status": "success"}
    return {"status": "error"}

def resolve_case(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    if policy_id in state.human_queue:
        state.human_queue[policy_id]["status"] = "resolved"
        state.human_queue[policy_id]["resolved_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        return {"status": "success"}
    return {"status": "error"}

def get_team_status(arguments: Dict) -> List[Dict]:
    return list(state.team_members.values())
