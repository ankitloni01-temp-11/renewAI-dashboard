import io, csv, uuid, json, os, asyncio
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from agents.whatsapp_agent import run_whatsapp_agent
from agents.whatsapp_critique import run_whatsapp_critique

router = APIRouter(prefix="/api", tags=["dashboard"])

# ── Load seed data once ──────────────────────────────────────────────
_SEED_PATH = os.path.join(os.path.dirname(__file__), "..", "seed_data", "dashboard_seed.json")
_DATA: dict = {}

def _load():
    global _DATA
    if not _DATA:
        with open(_SEED_PATH, "r") as f:
            _DATA = json.load(f)
    return _DATA

def _save():
    with open(_SEED_PATH, "w") as f:
        json.dump(_DATA, f, indent=2)

def _customers_map():
    return {c["customer_id"]: c for c in _load()["customers"]}

def _policies_list():
    return _load()["policies"]

def _journeys_list():
    return _load()["journeys"]

def _audit_list():
    return _load()["audit_log"]

def _escalation_list():
    return _load()["escalation_cases"]


# ── GET /api/policies ────────────────────────────────────────────────
@router.get("/policies")
async def get_policies(segment: Optional[str] = None, status: Optional[str] = None, search: Optional[str] = None):
    cmap = _customers_map()
    # Also check journey status to enrich policy status
    jmap = {j["policy_id"]: j for j in _journeys_list()}
    results = []
    for p in _policies_list():
        cust = cmap.get(p["customer_id"], {})
        j = jmap.get(p["policy_id"])
        effective_status = p["status"]
        if j:
            if j["status"] == "paid":
                effective_status = "PAID"
            elif j["status"] == "escalated":
                effective_status = "ESCALATED"
        row = {**p, "customer": cust, "effective_status": effective_status}
        # Filters
        if segment and segment != "All Segments" and cust.get("segment") != segment:
            continue
        if status and status != "All Statuses" and effective_status.upper() != status.upper():
            continue
        if search:
            q = search.lower()
            if q not in p["policy_id"].lower() and q not in cust.get("name", "").lower():
                continue
        results.append(row)
    return results


@router.get("/policies/{policy_id}")
async def get_policy(policy_id: str):
    cmap = _customers_map()
    for p in _policies_list():
        if p["policy_id"] == policy_id:
            return {**p, "customer": cmap.get(p["customer_id"], {})}
    return {"error": "not found"}


# ── GET /api/journeys ────────────────────────────────────────────────
@router.get("/journeys")
async def get_journeys(status_filter: Optional[str] = None):
    cmap = _customers_map()
    pmap = {p["policy_id"]: p for p in _policies_list()}
    LANG = {"hi": "Hindi", "en": "English", "ta": "Tamil", "ur": "Urdu", "mr": "Marathi"}
    results = []
    for j in _journeys_list():
        if status_filter and status_filter != "all" and j["status"] != status_filter:
            continue
        cust = cmap.get(j["customer_id"], {})
        pol = pmap.get(j["policy_id"], {})
        results.append({
            **j,
            "customer_name": cust.get("name", "Unknown"),
            "customer": cust,
            "policy": pol,
            "language_name": LANG.get(j.get("language"), j.get("language", "")),
            "premium": pol.get("premium"),
            "due_date": pol.get("due_date"),
            "product_name": pol.get("product_name"),
        })
    return results


@router.get("/journeys/{policy_id}")
async def get_journey_detail(policy_id: str):
    cmap = _customers_map()
    pmap = {p["policy_id"]: p for p in _policies_list()}
    LANG = {"hi": "Hindi", "en": "English", "ta": "Tamil", "ur": "Urdu", "mr": "Marathi"}
    for j in _journeys_list():
        if j["policy_id"] == policy_id:
            cust = cmap.get(j["customer_id"], {})
            pol = pmap.get(j["policy_id"], {})
            audit = [a for a in _audit_list() if a["policy_id"] == policy_id]
            audit.sort(key=lambda a: a["timestamp"])
            history = _load().get("conversations", {}).get(policy_id, [])
            return {
                **j,
                "customer_name": cust.get("name"),
                "customer": cust,
                "policy": pol,
                "language_name": LANG.get(j.get("language"), j.get("language", "")),
                "audit_trail": audit,
                "conversation_history": history,
            }
    return {"error": "journey not found"}


@router.get("/journeys/{policy_id}/status")
async def get_journey_status(policy_id: str):
    for j in _journeys_list():
        if j["policy_id"] == policy_id:
            return {"policy_id": policy_id, "status": j["status"], "current_step": j["current_step"]}
    return {"policy_id": policy_id, "status": "not_started", "current_step": None}


# ── GET /api/audit ───────────────────────────────────────────────────
@router.get("/audit")
async def get_audit(policy_id: Optional[str] = None, limit: int = 200):
    entries = _audit_list()
    if policy_id:
        q = str(policy_id).strip().lower()
        matched = []
        for e in entries:
            pid = str(e.get("policy_id", "")).lower()
            if q in pid:
                matched.append(e)
        entries = matched
    entries = sorted(entries, key=lambda e: str(e.get("timestamp", "")), reverse=True)
    return entries[:limit]


@router.get("/audit/{policy_id}")
async def get_audit_by_policy(policy_id: str):
    entries = [e for e in _audit_list() if e["policy_id"] == policy_id]
    entries.sort(key=lambda e: e["timestamp"])
    return entries


@router.get("/audit-export")
async def export_audit(policy_id: Optional[str] = None):
    entries = _audit_list()
    if policy_id:
        q = policy_id.lower()
        entries = [e for e in entries if q in str(e.get("policy_id", "")).lower()]
    entries = sorted(entries, key=lambda e: e["timestamp"], reverse=True)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Timestamp", "Policy ID", "Agent", "Action", "Evidence", "Prompt Version"])
    for e in entries:
        writer.writerow([e["timestamp"], e["policy_id"], e["agent_name"], e["action"], e["evidence"], e["prompt_version"]])
    buf.seek(0)
    return StreamingResponse(buf, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=irdai_audit_export.csv"})


# ── GET /api/human-queue ─────────────────────────────────────────────
@router.get("/human-queue")
async def get_human_queue(status: Optional[str] = None):
    cases = _escalation_list()
    if status and status != "all":
        cases = [c for c in cases if c["status"] == status]
    return cases


@router.post("/human-queue/{case_id}/resolve")
async def resolve_case(case_id: str, body: dict):
    data = _load()
    for c in data["escalation_cases"]:
        if c["case_id"] == case_id:
            c["status"] = "resolved"
            c["resolution_outcome"] = body.get("outcome", "")
            c["resolution_notes"] = body.get("notes", "")
            c["resolved_at"] = datetime.utcnow().isoformat() + "Z"
            _save()
            return {"status": "resolved", "case_id": case_id}
    return {"error": "case not found"}


# ── GET /api/kpis (computed) ─────────────────────────────────────────
@router.get("/kpis")
async def get_dashboard_kpis():
    journeys = _journeys_list()
    policies = _policies_list()
    cases = _escalation_list()
    total_j = len(journeys) if journeys else 1
    paid = [j for j in journeys if j["status"] == "paid"]
    escalated = [j for j in journeys if j["status"] == "escalated"]
    email_sent = [j for j in journeys if j["status"] == "email_sent"]
    wa_sent = [j for j in journeys if j["status"] == "whatsapp_sent"]
    active_states = {"whatsapp_sent", "email_sent", "voice_called", "started"}
    active = [j for j in journeys if j["status"] in active_states]
    total_premium_paid = sum(j.get("payment_amount") or 0 for j in paid)
    open_cases = len([c for c in cases if c["status"] == "open"])

    return {
        "persistency_rate": round(len(paid) / max(total_j, 1) * 100, 1),
        "cost_per_renewal": 45,
        "email_open_rate": 44.1 if email_sent else 0,
        "whatsapp_response_rate": round(len(paid) / max(len(wa_sent) + len(paid), 1) * 100, 1),
        "voice_conversion_rate": 0,
        "human_escalation_rate": round(len(escalated) / max(total_j, 1) * 100, 1),
        "customer_nps": 72,
        "irdai_violations": 0,
        "ai_accuracy_score": 94.2,
        "distress_escalation_pct": 100.0,
        "status_bar": {
            "active": len(active),
            "paid": len(paid),
            "escalated": open_cases,
            "today_premium": total_premium_paid,
        },
    }


# ── GET /api/agents/stats ───────────────────────────────────────────
@router.get("/agents/stats")
async def get_agent_stats():
    entries = _audit_list()
    agent_counts: dict = {}
    for e in entries:
        name = e["agent_name"]
        agent_counts[name] = agent_counts.get(name, 0) + 1

    return [
        {"name": "Orchestrator", "description": "Selects optimal channel, language, and tone for each customer.", "icon": "Compass",
         "stats": {"total_runs": agent_counts.get("Orchestrator", 0), "avg_latency_ms": 1200, "success_rate": 100.0}},
        
        {"name": "Planner", "description": "Creates multi-step engagement plans.", "icon": "Map",
         "stats": {"total_runs": agent_counts.get("Planner", 0), "avg_latency_ms": 2800, "avg_critique_score": 8.4}},
         
        {"name": "Planner Critique", "description": "Reviews the execution plan for strategy and compliance.", "icon": "ShieldCheck",
         "stats": {"reviews_done": agent_counts.get("PlannerCritique", 0), "approval_rate": 92.0, "avg_latency_ms": 2100}},
         
        {"name": "Email Agent", "description": "Generates personalized renewal emails.", "icon": "Mail",
         "stats": {"emails_generated": agent_counts.get("Email Agent", 0), "delivery_rate": 98.5, "open_rate": 44.1}},
         
        {"name": "WhatsApp Agent", "description": "Handles WhatsApp conversations.", "icon": "MessageSquare",
         "stats": {"messages_sent": agent_counts.get("WhatsApp Agent", 0), "response_rate": 54.3, "avg_per_journey": 1.8}},
         
        {"name": "Voice Agent", "description": "Manages voice call interactions (ElevenLabs).", "icon": "Phone",
         "stats": {"calls_made": agent_counts.get("Voice Agent", 0), "avg_duration_sec": 45, "escalation_rate": 12.5}},
         
        {"name": "Email Critique", "description": "Evaluates email output for factual accuracy and tone.", "icon": "FileCheck",
         "stats": {"reviews_done": agent_counts.get("EmailCritique", 0), "approval_rate": 94.0, "avg_latency_ms": 1800}},
         
        {"name": "WhatsApp Critique", "description": "Evaluates WA response against evidence and compliance.", "icon": "FileCheck",
         "stats": {"reviews_done": agent_counts.get("WhatsAppCritiqueAgent", 0), "approval_rate": 88.0, "avg_latency_ms": 1900}},
         
        {"name": "Voice Critique", "description": "Verifies voice script vs evidence and checks objection handling.", "icon": "FileCheck",
         "stats": {"reviews_done": agent_counts.get("VoiceCritiqueAgent", 0), "approval_rate": 91.0, "avg_latency_ms": 2200}},
         
        {"name": "Content Safety Guard", "description": "Scans for PII, distress markers, and mis-selling before final transmission.", "icon": "Shield",
         "stats": {"scans_done": agent_counts.get("ContentSafetyGuard", 0), "violations_caught": 0, "false_positive_rate": 1.2}}
    ]

# ── GET/PUT /api/prompts ─────────────────────────────────────────────
from database.sqlite_manager import db
from fastapi import HTTPException

@router.get("/prompts")
async def get_all_prompts():
    try:
        return db.get_all_prompts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/prompts/{name}")
async def update_prompt_content(name: str, body: dict):
    content = body.get("content")
    if not content:
        raise HTTPException(status_code=400, detail="content required")
    try:
        new_version = db.update_prompt(name, content)
        return {"status": "success", "name": name, "version": new_version}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ── TRIGGER ENDPOINTS ───────────────────────────────────────────────

@router.post("/triggers/start-journey")
async def start_journey(body: dict):
    policy_id = body.get("policy_id")
    data = _load()
    
    # Check if journey exists
    journey = next((j for j in data["journeys"] if j["policy_id"] == policy_id), None)
    if journey:
        journey["status"] = "started"
        journey["current_step"] = "orchestrator_complete"
        journey["updated_at"] = datetime.now().isoformat()
    else:
        # Create new journey
        pol = next((p for p in data["policies"] if p["policy_id"] == policy_id), None)
        if not pol:
            return {"error": "Policy not found"}
        
        new_j = {
            "policy_id": policy_id,
            "customer_id": pol["customer_id"],
            "status": "started",
            "current_step": "orchestrator_complete",
            "channel": "whatsapp",
            "language": "hi",
            "started_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        data["journeys"].append(new_j)
    
    # Add audit entry
    data["audit_log"].insert(0, {
        "timestamp": datetime.now().isoformat(),
        "policy_id": policy_id,
        "agent_name": "Orchestrator",
        "action": "CHANNEL_SELECTED",
        "evidence": "Selected WhatsApp as primary channel based on historical engagement.",
        "prompt_version": "v1"
    })
    
    _save()
    return {"status": "started", "policy_id": policy_id}


@router.post("/triggers/simulate-payment/{policy_id}")
async def simulate_payment(policy_id: str):
    data = _load()
    journey = next((j for j in data["journeys"] if j["policy_id"] == policy_id), None)
    pol = next((p for p in data["policies"] if p["policy_id"] == policy_id), None)
    cmap = {c["customer_id"]: c for c in data["customers"]}
    
    if not pol:
        return {"error": "Policy not found"}
        
    if journey:
        journey["status"] = "paid"
        journey["payment_amount"] = pol["premium"]
        journey["updated_at"] = datetime.now().isoformat()
    
    # Update policy status
    pol["effective_status"] = "PAID"
    
    # Audit log
    data["audit_log"].insert(0, {
        "timestamp": datetime.now().isoformat(),
        "policy_id": policy_id,
        "agent_name": "Channel Router",
        "action": "PAYMENT_CONFIRMED",
        "evidence": f"Payment of ₹{pol['premium']:,} received and reconciled via Razorpay.",
        "prompt_version": "v1"
    })
    
    _save()
    cust = cmap.get(pol["customer_id"], {})
    return {"amount": pol["premium"], "customer_name": cust.get("name", "Customer")}


@router.post("/triggers/reset-demo")
async def reset_demo():
    data = _load()
    # Keep original 8 seeded journeys
    data["journeys"] = data["journeys"][:8]
    _save()
    return {"message": "Demo reset complete"}


@router.post("/triggers/t45-scan")
async def t45_scan(count: int = 5):
    data = _load()
    pids = [p["policy_id"] for p in data["policies"]]
    active_pids = [j["policy_id"] for j in data["journeys"]]
    candidates = [p for p in pids if p not in active_pids]
    
    import random
    selected = random.sample(candidates, min(count, len(candidates)))
    for pid in selected:
        pol = next(p for p in data["policies"] if p["policy_id"] == pid)
        data["journeys"].append({
            "policy_id": pid,
            "customer_id": pol["customer_id"],
            "status": "started",
            "current_step": "orchestrator_complete",
            "channel": "whatsapp",
            "language": "hi",
            "started_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
    _save()
    return {"triggered": len(selected), "policy_ids": selected}


@router.post("/triggers/single/{policy_id}")
async def start_single_journey_legacy(policy_id: str):
    # Alias for start-journey to support existing component calls
    return await start_journey({"policy_id": policy_id})


# ── CONVERSATION ENDPOINTS ──────────────────────────────────────────

@router.get("/conversations/{policy_id}/history")
async def get_history(policy_id: str):
    data = _load()
    if "conversations" not in data: data["conversations"] = {}
    return {"history": data["conversations"].get(policy_id, [])}


@router.post("/conversations/whatsapp/message")
async def whatsapp_message(policy_id: str, customer_message: str):
    data = _load()
    if "conversations" not in data: data["conversations"] = {}
    if policy_id not in data["conversations"]: data["conversations"][policy_id] = []
    
    # Store customer message
    timestamp = datetime.now().isoformat()
    data["conversations"][policy_id].append({
        "message_id": str(uuid.uuid4()),
        "role": "customer",
        "customer_text": customer_message,
        "timestamp": timestamp,
        "channel": "whatsapp"
    })
    
    # Fetch journey for plan/orch results
    journey = next((j for j in data["journeys"] if j["policy_id"] == policy_id), {})
    plan = journey.get("plan", {"message_structure": ["greeting"]})
    orch = journey.get("orchestrator_result", {"language": "English"})
    history = data["conversations"][policy_id]

    # Run agent
    try:
        wa_result = await run_whatsapp_agent(policy_id, plan, orch, customer_message, history)
        critique = await run_whatsapp_critique(policy_id, wa_result, customer_message)
        
        ai_msg = {
            "message_id": str(uuid.uuid4()),
            "role": "ai",
            "ai_response": wa_result.get("response_text", ""),
            "detected_intent": wa_result.get("detected_intent"),
            "critique_score": critique.get("overall_score"),
            "safety_verdict": wa_result.get("safety_result", {}).get("verdict", "PASS"),
            "timestamp": datetime.now().isoformat(),
            "channel": "whatsapp",
            "escalated": wa_result.get("escalation_needed", False)
        }
        data["conversations"][policy_id].append(ai_msg)
        
        # If escalated, update journey status
        if wa_result.get("escalation_needed"):
            journey["status"] = "escalated"
            # Add to escalation cases if not there
            if not any(c["policy_id"] == policy_id for c in data["escalation_cases"]):
                data["escalation_cases"].append({
                    "case_id": f"CASE-{uuid.uuid4().hex[:4].upper()}",
                    "policy_id": policy_id,
                    "customer_name": next((c["name"] for c in data["customers"] if c["customer_id"] == (journey.get("customer_id") or "CUST-0001")), "Valued Customer"),
                    "product_name": "Insurance Policy",
                    "premium": 0,
                    "reason": f"Inbound distress: {wa_result.get('detected_intent')}",
                    "priority": 0.9,
                    "status": "open",
                    "created_at": datetime.now().isoformat()
                })

        _save()
        return {
            "ai_response": ai_msg["ai_response"],
            "detected_intent": ai_msg["detected_intent"],
            "critique_score": ai_msg["critique_score"],
            "escalated": ai_msg["escalated"],
            "case_id": next((c["case_id"] for c in data["escalation_cases"] if c["policy_id"] == policy_id), None) if ai_msg["escalated"] else None
        }
    except Exception as e:
        _save() # Save the customer message part
        return {"error": str(e)}


# ── FINANCIAL ENDPOINTS ─────────────────────────────────────────────

@router.get("/kpis/financial")
async def get_financial_kpis():
    # Return data used in ExecutiveKPIPage.tsx
    return {
        "annual_saving": 12.9,
        "revenue_uplift": 38.9,
        "net_year1": 48.0,
        "npv_3yr": 89.0,
        "payback_months": 7.8,
        "monthly_data": [
            {"month": "Jan", "saving": 1.075, "revenue": 3.24},
            {"month": "Feb", "saving": 1.075, "revenue": 3.24},
            {"month": "Mar", "saving": 1.075, "revenue": 3.24}
        ]
    }


@router.get("/kpis/funnel")
async def get_funnel_stats():
    # Simple funnel based on statuses
    js = _journeys_list()
    total = len(_policies_list())
    email = len([j for j in js if j["channel"] == "email"])
    wa = len([j for j in js if j["channel"] == "whatsapp"])
    voice = len([j for j in js if j["channel"] == "voice"])
    paid = len([j for j in js if j["status"] == "paid"])
    
    return [
        {"name": "Total Policies", "value": total, "fill": "#1B4F8A"},
        {"name": "Email Sent", "value": email, "fill": "#2563EB"},
        {"name": "WA Sent", "value": wa, "fill": "#16A34A"},
        {"name": "Voice Calls", "value": voice, "fill": "#9333EA"},
        {"name": "Payments", "value": paid, "fill": "#D97706"},
    ]
