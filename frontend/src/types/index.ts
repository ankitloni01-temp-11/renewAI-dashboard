export interface Customer {
  customer_id: string; name?: string; full_name?: string; first_name?: string; last_name?: string
  age: number; phone: string; email: string; preferred_language: string
  preferred_channel: string; preferred_contact_time: string; segment: string
  tenure_years: number; complaint_count: number; city: string; state: string
}
export interface Policy {
  policy_id: string; customer_id: string; product_name: string; product_type: string
  premium_amount: number; sum_assured: number; due_date: string; status: string
  payment_history?: Array<{ year: number; status: string }>
  fund_value?: number; nav_change_pct?: number; maturity_date?: string; projected_maturity_value?: number
}
export interface Journey {
  journey_id: string; policy_id: string; customer_id: string; status: string
  current_step?: string; channel?: string; language?: string
  started_at?: string; updated_at?: string; escalation_reason?: string
  escalated_at?: string; paid_at?: string; payment_amount?: number
}
export interface QueueCase {
  case_id: string; policy_id: string; customer_name: string
  priority: 'URGENT' | 'STANDARD'; reason: string; escalation_summary: string
  escalated_at: string; sla_hours: number; assigned_to?: string; status: string
  premium_amount?: number; risk_level?: string; preferred_language?: string
  channel_detected?: string; briefing_note?: string; recommended_approach?: string
  recommended_resolution_options?: string[]; assigned_specialist_type?: string
  conversation_history?: Message[]
}
export interface AuditEntry {
  trace_id: string; policy_id: string; step_number: number; agent_name: string
  action: string; input_summary: string; output_summary: string
  model_used?: string; latency_ms?: number; token_count_in?: number; token_count_out?: number
  critique_score?: number; verdict?: string; timestamp: string; full_output?: Record<string, unknown>
}
export interface Message {
  message_id: string; policy_id: string; role: 'customer' | 'ai'
  customer_text?: string; ai_response?: string; detected_intent?: string
  sentiment?: string; critique_score?: number; safety_verdict?: string
  timestamp: string; channel: string
}
export interface KPIs {
  persistency_rate: number; cost_per_renewal: number; email_open_rate: number
  whatsapp_response_rate: number; voice_conversion_rate: number
  human_escalation_rate: number; customer_nps: number; irdai_violations: number
  ai_accuracy_score: number; distress_escalation_pct: number
  total_journeys: number; paid_journeys: number; escalated_journeys: number
  active_journeys: number; payments_today: number
}
export type UserRole = 'renewal_head' | 'senior_rrm' | 'revival_specialist' | 'compliance_handler' | 'ai_ops_manager' | 'admin'
export interface User { id: string; name: string; role: UserRole; employee_id?: string }
