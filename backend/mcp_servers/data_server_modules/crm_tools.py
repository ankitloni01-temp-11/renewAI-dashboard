"""CRM tool handlers for the Data Server."""
from typing import Dict, Any, List
from . import shared_state as state

def get_customer(arguments: Dict) -> Dict:
    customer_id = arguments.get("customer_id")
    return state.customers.get(customer_id, {})

def get_policy(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    return state.policies.get(policy_id, {})

def get_propensity_score(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    return state.propensity.get(policy_id, {})

def search_policies_due(arguments: Dict) -> List[Dict]:
    days = arguments.get("days", 30)
    # Simple mock check - in real app would check dates
    return list(state.policies.values())[:10]

def get_customer_by_policy(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    policy = state.policies.get(policy_id, {})
    customer_id = policy.get("customer_id")
    return state.customers.get(customer_id, {})
