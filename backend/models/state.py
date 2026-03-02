from typing import TypedDict, Optional, List, Dict, Any

class RenewalState(TypedDict):
    policy_id: str
    customer_id: str
    customer_data: Dict[str, Any]
    policy_data: Dict[str, Any]
    propensity_data: Dict[str, Any]
    journey_state: Dict[str, Any]
    plan: Optional[Dict[str, Any]]
    critique_result: Optional[Dict[str, Any]]
    execution_result: Optional[Dict[str, Any]]
    safety_result: Optional[Dict[str, Any]]
    conversation_history: List[Dict[str, Any]]
    attempt: int
    escalation_reason: Optional[str]
    status: str
    current_channel: Optional[str]
    audit_entries: List[Dict[str, Any]]
