from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class CustomerSegment(str, Enum):
    wealth_builder = "wealth_builder"
    budget_conscious = "budget_conscious"
    loyal_long_term = "loyal_long_term"
    new_customer = "new_customer"
    hni = "hni"
    tech_savvy = "tech_savvy"


class Channel(str, Enum):
    email = "email"
    whatsapp = "whatsapp"
    voice = "voice"
    human = "human"


class Language(str, Enum):
    english = "English"
    hindi = "Hindi"
    marathi = "Marathi"
    bengali = "Bengali"
    tamil = "Tamil"
    telugu = "Telugu"
    kannada = "Kannada"
    malayalam = "Malayalam"
    gujarati = "Gujarati"


class JourneyStatus(str, Enum):
    started = "started"
    planning = "planning"
    executing = "executing"
    email_sent = "email_sent"
    whatsapp_sent = "whatsapp_sent"
    voice_called = "voice_called"
    paid = "paid"
    escalated = "escalated"
    lapsed = "lapsed"
    completed = "completed"
    error = "error"


class Priority(str, Enum):
    urgent = "urgent"
    standard = "standard"
    compliance = "compliance"


class QueueStatus(str, Enum):
    open = "open"
    assigned = "assigned"
    on_hold = "on_hold"
    resolved = "resolved"


class Customer(BaseModel):
    customer_id: str
    name: str
    age: int
    phone: str
    email: str
    preferred_language: str
    preferred_channel: str
    preferred_contact_time: str
    segment: str
    tenure_years: int
    complaint_count: int
    city: str
    state: str


class Policy(BaseModel):
    policy_id: str
    customer_id: str
    product_name: str
    product_type: str
    premium_amount: float
    sum_assured: float
    due_date: str
    payment_history: List[Dict[str, Any]]
    status: str
    fund_value: Optional[float] = None
    nav_change_pct: Optional[float] = None
    maturity_date: Optional[str] = None
    projected_maturity_value: Optional[float] = None


class PropensityScore(BaseModel):
    policy_id: str
    propensity_score: int
    risk_level: str
    factors: List[str]


class JourneyStep(BaseModel):
    step: str
    agent: str
    channel: Optional[str] = None
    status: str
    timestamp: str
    message_preview: Optional[str] = None
    critique_score: Optional[float] = None
    verdict: Optional[str] = None


class Journey(BaseModel):
    policy_id: str
    customer_id: str
    status: JourneyStatus
    current_step: str
    steps: List[JourneyStep] = []
    conversation_history: List[Dict[str, Any]] = []
    escalation_reason: Optional[str] = None
    started_at: str
    updated_at: str
    paid_at: Optional[str] = None
    payment_amount: Optional[float] = None
    attempt_count: int = 0


class QueueCase(BaseModel):
    case_id: str
    policy_id: str
    customer_id: str
    priority: Priority
    status: QueueStatus
    escalation_reason: str
    escalation_detail: str
    assigned_to: Optional[str] = None
    assigned_at: Optional[str] = None
    resolved_at: Optional[str] = None
    resolution: Optional[str] = None
    resolution_notes: Optional[str] = None
    briefing_note: Optional[str] = None
    recommended_approach: Optional[str] = None
    detected_sentiment: Optional[str] = None
    sla_hours: int
    escalated_at: str
    conversation_history: List[Dict[str, Any]] = []


class AuditEvent(BaseModel):
    event_id: str
    trace_id: str
    policy_id: str
    step_number: int
    agent_name: str
    action: str
    input_summary: str
    output_summary: str
    full_input: Optional[Dict[str, Any]] = None
    full_output: Optional[Dict[str, Any]] = None
    model_used: Optional[str] = None
    latency_ms: Optional[int] = None
    token_count_in: Optional[int] = None
    token_count_out: Optional[int] = None
    critique_score: Optional[float] = None
    verdict: Optional[str] = None
    timestamp: str


class WhatsAppMessage(BaseModel):
    policy_id: str
    customer_message: str


class VoiceTurn(BaseModel):
    policy_id: str
    call_id: str
    customer_text: str


class ResolveCase(BaseModel):
    case_id: str
    resolution: str
    resolution_notes: str
    resolved_by: str


class KPI(BaseModel):
    name: str
    baseline: Any
    target: Any
    actual: Any
    unit: str
    status: str  # on_track, close, behind
    trend: str   # up, down, stable
