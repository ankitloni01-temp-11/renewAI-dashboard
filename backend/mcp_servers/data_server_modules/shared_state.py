"""Shared in-memory state for the modular Data Server."""
import os
import json
import sys
from typing import Dict, Any, List

# Core state dictionaries
# These will be populated by the load() method
customers: Dict[str, Any] = {}
policies: Dict[str, Any] = {}
propensity: Dict[str, Any] = {}
journeys: Dict[str, Any] = {}
audit_trail: List[Dict[str, Any]] = []
conversations: Dict[str, List[Dict[str, Any]]] = {}
human_queue: Dict[str, Any] = {}
team_members: Dict[str, Any] = {}
messages: Dict[str, Dict[str, Any]] = {}

SEED_DIR = "/home/labuser/VSCODE_training/renewai-demo/backend/seed_data"

def load():
    """Load all seed data into memory."""
    global customers, policies, propensity, team_members
    
    # Customers
    try:
        with open(os.path.join(SEED_DIR, "customers.json")) as f:
            data = json.load(f)
            customers = {c["customer_id"]: c for c in data}
    except Exception as e:
        print(f"Error loading customers: {e}", file=sys.stderr)

    # Policies
    try:
        with open(os.path.join(SEED_DIR, "policies.json")) as f:
            data = json.load(f)
            policies = {p["policy_id"]: p for p in data}
    except Exception as e:
        print(f"Error loading policies: {e}", file=sys.stderr)

    # Propensity
    try:
        with open(os.path.join(SEED_DIR, "propensity_scores.json")) as f:
            data = json.load(f)
            propensity = {p["policy_id"]: p for p in data}
    except Exception as e:
        print(f"Error loading propensity: {e}", file=sys.stderr)
        
    # Team
    try:
        with open(os.path.join(SEED_DIR, "team_members.json")) as f:
            data = json.load(f)
            team_members = {m["employee_id"]: m for m in data}
    except Exception as e:
        print(f"Error loading team: {e}", file=sys.stderr)

# Call load on import
load()
