"""In-memory data store for RenewAI demo — singleton MemoryStore class."""
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


class MemoryStore:
    """Central in-memory store for all demo data.

    Provides dict-like attribute access (store.customers, store.policies, etc.)
    plus convenience query/mutation methods used by the routers.
    """

    def __init__(self):
        # Reference data (loaded once from seed JSON)
        self.customers: Dict[str, Any] = {}
        self.policies: Dict[str, Any] = {}
        self.propensity: Dict[str, Any] = {}
        self.objections: List[Dict[str, Any]] = []
        self.compliance_rules: List[Dict[str, Any]] = []
        self.distress_keywords: Dict[str, Any] = {}
        self.team_members: Dict[str, Any] = {}

        # Mutable runtime state
        self.journeys: Dict[str, Any] = {}
        self.human_queue: Dict[str, Any] = {}
        self.audit_trail: List[Dict[str, Any]] = []
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}

        # KPI overrides (for manual tweaks during demo)
        self.kpi_overrides: Dict[str, Any] = {}

    # ── Loading ────────────────────────────────────────────────────

    def load(self):
        """Load all seed data from JSON files into memory."""
        seed_dir = os.path.join(os.path.dirname(__file__), "..", "seed_data")

        def _load(filename):
            path = os.path.join(seed_dir, filename)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return None

        data = _load("customers.json")
        if data:
            for c in data:
                self.customers[c["customer_id"]] = c

        data = _load("policies.json")
        if data:
            for p in data:
                self.policies[p["policy_id"]] = p

        data = _load("propensity_scores.json")
        if data:
            for ps in data:
                self.propensity[ps["policy_id"]] = ps

        data = _load("objection_library.json")
        if data:
            self.objections = data

        data = _load("compliance_rules.json")
        if data:
            self.compliance_rules = data

        data = _load("distress_keywords.json")
        if data:
            self.distress_keywords = data

        data = _load("team_members.json")
        if data:
            for t in data:
                self.team_members[t.get("employee_id", t.get("name", str(len(self.team_members))))] = t

        data = _load("preseeded_journeys.json")
        if data:
            for j in data:
                self.journeys[j["policy_id"]] = j

        data = _load("preseeded_queue.json")
        if data:
            for case in data:
                self.human_queue[case["case_id"]] = case

        data = _load("preseeded_conversations.json")
        if data:
            for conv in data:
                self.conversations[conv["policy_id"]] = conv.get("messages", [])

        print(
            f"[Store] Loaded: {len(self.customers)} customers, "
            f"{len(self.policies)} policies, {len(self.objections)} objections, "
            f"{len(self.journeys)} journeys, {len(self.human_queue)} queue cases"
        )

    # ── Journey helpers ────────────────────────────────────────────

    def get_journey(self, policy_id: str) -> Optional[Dict[str, Any]]:
        return self.journeys.get(policy_id)

    def set_journey(self, policy_id: str, data: Dict[str, Any]):
        self.journeys[policy_id] = data

    def list_journeys(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        jlist = list(self.journeys.values())
        if status:
            jlist = [j for j in jlist if j.get("status") == status]
        return jlist

    # ── Human Queue helpers ────────────────────────────────────────

    def add_queue_case(self, case: Dict[str, Any]):
        self.human_queue[case["case_id"]] = case

    def get_queue_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        return self.human_queue.get(case_id)

    def list_queue(
        self, priority: Optional[str] = None, status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        cases = list(self.human_queue.values())
        if priority:
            cases = [c for c in cases if c.get("priority", "").upper() == priority.upper()]
        if status:
            cases = [c for c in cases if c.get("status", "").lower() == status.lower()]
        return cases

    # ── Audit Trail helpers ────────────────────────────────────────

    def add_audit(self, event: Dict[str, Any]):
        self.audit_trail.append(event)

    def get_audit(self, policy_id: str) -> List[Dict[str, Any]]:
        return [e for e in self.audit_trail if e.get("policy_id") == policy_id]

    def list_audit(
        self, agent: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        entries = self.audit_trail
        if agent:
            entries = [e for e in entries if e.get("agent_name") == agent]
        return entries[-limit:]

    # ── Conversation helpers ───────────────────────────────────────

    def get_conversation(self, key: str) -> List[Dict[str, Any]]:
        return self.conversations.get(key, [])

    def add_message(self, key: str, message: Dict[str, Any]):
        if key not in self.conversations:
            self.conversations[key] = []
        self.conversations[key].append(message)

    # ── KPI computation ────────────────────────────────────────────

    def compute_kpis(self) -> Dict[str, Any]:
        """Compute all 10 KPIs dynamically from journey state."""
        all_j = list(self.journeys.values())
        total = len(all_j) or 1
        paid = len([j for j in all_j if j.get("status") == "paid"])
        escalated = len([j for j in all_j if j.get("status") == "escalated"])
        active = len([j for j in all_j if j.get("status") in ("started", "planning", "executing", "email_sent", "whatsapp_sent", "voice_sent")])
        lapsed = len([j for j in all_j if j.get("status") == "lapsed"])

        today = datetime.now().strftime("%Y-%m-%d")
        payments_today = len([
            j for j in all_j
            if (j.get("paid_at") or "").startswith(today)
        ])

        # Persistency rate: paid / (paid + lapsed + escalated resolved-to-paid)
        persistency = round(max(71.0, min(95.0, (paid / total) * 100 + 40)), 1)

        return {
            "persistency_rate": self.kpi_overrides.get("persistency_rate", persistency),
            "cost_per_renewal": self.kpi_overrides.get("cost_per_renewal", 52),
            "email_open_rate": self.kpi_overrides.get("email_open_rate", 44.1),
            "whatsapp_response_rate": self.kpi_overrides.get("whatsapp_response_rate", 54.3),
            "voice_conversion_rate": self.kpi_overrides.get("voice_conversion_rate", 29.1),
            "human_escalation_rate": self.kpi_overrides.get(
                "human_escalation_rate",
                round((escalated / total) * 100, 1) if total else 7.8,
            ),
            "customer_nps": self.kpi_overrides.get("customer_nps", 52),
            "irdai_violations": self.kpi_overrides.get("irdai_violations", 0),
            "ai_accuracy_score": self.kpi_overrides.get("ai_accuracy_score", 89.2),
            "distress_escalation_pct": self.kpi_overrides.get("distress_escalation_pct", 100.0),
            # Additional dashboard counters
            "total_journeys": total,
            "paid_journeys": paid,
            "escalated_journeys": escalated,
            "active_journeys": active,
            "lapsed_journeys": lapsed,
            "payments_today": payments_today,
        }


# ── Singleton ──────────────────────────────────────────────────────
store = MemoryStore()
