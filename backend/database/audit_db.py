import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List
import uuid
from pathlib import Path

class AuditDatabase:
    """
    SQLite audit trail database
    Append-only, immutable logging of all agent actions
    """
    
    def __init__(self, db_path: str = "database/audit.db"):
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
    
    def _init_schema(self):
        """Initialize audit database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Audit logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                trace_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                agent_id TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                step_sequence INTEGER,
                customer_id TEXT,
                policy_id TEXT,
                channel TEXT,
                
                input_prompt TEXT,
                input_context JSON,
                agent_response TEXT,
                response_metadata JSON,
                
                critique_result JSON,
                critique_count INTEGER DEFAULT 0,
                critique_passed BOOLEAN,
                
                safety_check JSON,
                safety_passed BOOLEAN,
                
                final_output TEXT,
                action TEXT,
                reason TEXT,
                
                execution_time_ms FLOAT,
                error_message TEXT,
                
                INDEX idx_trace_id (trace_id),
                INDEX idx_customer_id (customer_id),
                INDEX idx_agent_id (agent_id),
                INDEX idx_timestamp (timestamp)
            )
        """)
        
        # Journey state history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS journey_history (
                id TEXT PRIMARY KEY,
                trace_id TEXT NOT NULL UNIQUE,
                customer_id TEXT NOT NULL,
                policy_id TEXT,
                trigger_event TEXT,
                channel TEXT,
                language TEXT,
                
                orchestrator_decision JSON,
                planner_output JSON,
                execution_results JSON,
                
                escalated BOOLEAN DEFAULT 0,
                escalation_reason TEXT,
                human_assigned_to TEXT,
                
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                duration_seconds FLOAT,
                
                INDEX idx_customer_id (customer_id),
                INDEX idx_trace_id (trace_id)
            )
        """)
        
        # Critique retry history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS critique_retries (
                id TEXT PRIMARY KEY,
                trace_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                attempt_number INTEGER,
                
                agent_output TEXT,
                critique_feedback TEXT,
                issues_found JSON,
                
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                INDEX idx_trace_id (trace_id),
                INDEX idx_agent_id (agent_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_agent_action(self, 
                        trace_id: str,
                        agent_id: str,
                        agent_type: str,
                        step_sequence: int,
                        customer_id: str,
                        policy_id: str,
                        channel: str,
                        input_prompt: str,
                        input_context: Dict,
                        agent_response: str,
                        response_metadata: Dict,
                        execution_time_ms: float,
                        error_message: str = None) -> str:
        """
        Log an agent action to audit trail
        Returns: log_id
        """
        log_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO audit_logs (
                id, trace_id, agent_id, agent_type, step_sequence,
                customer_id, policy_id, channel,
                input_prompt, input_context, agent_response, response_metadata,
                execution_time_ms, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            log_id, trace_id, agent_id, agent_type, step_sequence,
            customer_id, policy_id, channel,
            input_prompt, json.dumps(input_context), agent_response, json.dumps(response_metadata),
            execution_time_ms, error_message
        ))
        
        conn.commit()
        conn.close()
        
        return log_id
    
    def log_critique_result(self, 
                           log_id: str,
                           critique_result: Dict,
                           critique_count: int,
                           critique_passed: bool) -> None:
        """Update log with critique results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE audit_logs 
            SET critique_result = ?, critique_count = ?, critique_passed = ?
            WHERE id = ?
        """, (json.dumps(critique_result), critique_count, critique_passed, log_id))
        
        conn.commit()
        conn.close()
    
    def log_safety_check(self, 
                        log_id: str,
                        safety_check: Dict,
                        safety_passed: bool,
                        final_output: str,
                        action: str,
                        reason: str = None) -> None:
        """Update log with safety check results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE audit_logs 
            SET safety_check = ?, safety_passed = ?, final_output = ?, action = ?, reason = ?
            WHERE id = ?
        """, (json.dumps(safety_check), safety_passed, final_output, action, reason, log_id))
        
        conn.commit()
        conn.close()
    
    def start_journey(self, 
                     trace_id: str,
                     customer_id: str,
                     policy_id: str,
                     trigger_event: str,
                     channel: str,
                     language: str) -> None:
        """Start a new journey trace"""
        journey_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO journey_history (
                id, trace_id, customer_id, policy_id, trigger_event, channel, language
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (journey_id, trace_id, customer_id, policy_id, trigger_event, channel, language))
        
        conn.commit()
        conn.close()
    
    def end_journey(self,
                   trace_id: str,
                   escalated: bool = False,
                   escalation_reason: str = None,
                   human_assigned_to: str = None) -> None:
        """End journey and mark escalation if needed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE journey_history 
            SET end_time = CURRENT_TIMESTAMP,
                duration_seconds = (julianday(CURRENT_TIMESTAMP) - julianday(start_time)) * 86400,
                escalated = ?,
                escalation_reason = ?,
                human_assigned_to = ?
            WHERE trace_id = ?
        """, (escalated, escalation_reason, human_assigned_to, trace_id))
        
        conn.commit()
        conn.close()
    
    def get_journey_trace(self, trace_id: str) -> Dict[str, Any]:
        """Retrieve full journey trace for investigation dashboard"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get journey summary
        cursor.execute("""
            SELECT * FROM journey_history WHERE trace_id = ?
        """, (trace_id,))
        journey = dict(cursor.fetchone()) if cursor.fetchone() else {}
        
        # Get all agent actions in sequence
        cursor.execute("""
            SELECT 
                id, agent_id, agent_type, step_sequence,
                input_prompt, agent_response, critique_result,
                safety_check, final_output, action, reason,
                execution_time_ms, error_message, timestamp
            FROM audit_logs 
            WHERE trace_id = ?
            ORDER BY step_sequence ASC
        """, (trace_id,))
        
        steps = [dict(row) for row in cursor.fetchall()]
        
        # Get critique retries
        cursor.execute("""
            SELECT * FROM critique_retries 
            WHERE trace_id = ?
            ORDER BY attempt_number ASC
        """, (trace_id,))
        
        retries = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "journey": journey,
            "steps": steps,
            "critiques": retries
        }