"""Payment tool handlers for the Data Server."""
import uuid
import time
from typing import Dict, Any, List
from . import shared_state as state

def generate_payment_link(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    amount = arguments.get("amount")
    link = f"https://pay.suraksha.com/renew/{str(uuid.uuid4())[:12]}"
    return {"status": "success", "payment_link": link, "amount": amount}

def check_payment_status(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    # In demo, we might check if a "paid" event happened in journeys
    journey = state.journeys.get(policy_id, {})
    return {"paid": journey.get("status") == "paid", "paid_at": journey.get("paid_at")}

def mark_payment(arguments: Dict) -> Dict:
    policy_id = arguments.get("policy_id")
    if policy_id in state.journeys:
        state.journeys[policy_id]["status"] = "paid"
        state.journeys[policy_id]["paid_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        return {"status": "success"}
    return {"status": "error", "message": "Journey not found"}

def generate_emi_plan(arguments: Dict) -> Dict:
    amount = arguments.get("amount", 0)
    months = arguments.get("months", 3)
    emi = amount / months
    return {
        "plan_type": "interest_free",
        "months": months,
        "emi_amount": round(emi, 2),
        "total_payable": amount
    }

def generate_revival_quotation(arguments: Dict) -> Dict:
    # Calculation for lapsed policy revival
    policy_id = arguments.get("policy_id")
    policy = state.policies.get(policy_id, {})
    premium = policy.get("premium_amount", 0)
    interest = premium * 0.05 # 5% late fee
    total = premium + interest
    return {
        "original_premium": premium,
        "revival_fee": round(interest, 2),
        "total_revival_amount": round(total, 2),
        "valid_until": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
