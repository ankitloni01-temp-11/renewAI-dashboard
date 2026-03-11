import google.generativeai as genai
from typing import Dict, Any, Optional
from datetime import datetime
import time
from config.settings import settings
from database.audit_db import AuditDatabase

genai.configure(api_key=settings.GEMINI_API_KEY)

class BaseAgent:
    """
    Base agent class using Gemini 2.0 Flash
    Handles common functionality: LLM calls, audit logging, prompt management
    """
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.audit_db = AuditDatabase(settings.AUDIT_DB_PATH)
        self.model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            generation_config={
                "temperature": settings.GEMINI_TEMPERATURE,
                "max_output_tokens": 2000
            }
        )
    
    def call_llm(self, prompt: str, context: Dict = None) -> str:
        """
        Call Gemini 2.0 Flash API
        
        Args:
            prompt: The prompt to send to LLM
            context: Optional context dict for audit logging
        
        Returns:
            LLM response text
        """
        try:
            start_time = time.time()
            
            response = self.model.generate_content(
                prompt,
                stream=False
            )
            
            execution_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return response.text, execution_time
        except Exception as e:
            print(f"LLM Error in {self.agent_id}: {str(e)}")
            raise
    
    def log_action(self,
                  trace_id: str,
                  step_sequence: int,
                  customer_id: str,
                  policy_id: str,
                  channel: str,
                  input_prompt: str,
                  input_context: Dict,
                  agent_response: str,
                  response_metadata: Dict = None,
                  execution_time_ms: float = 0,
                  error_message: str = None) -> str:
        """Log agent action to audit trail"""
        return self.audit_db.log_agent_action(
            trace_id=trace_id,
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            step_sequence=step_sequence,
            customer_id=customer_id,
            policy_id=policy_id,
            channel=channel,
            input_prompt=input_prompt,
            input_context=input_context,
            agent_response=agent_response,
            response_metadata=response_metadata or {},
            execution_time_ms=execution_time_ms,
            error_message=error_message
        )
    
    def log_critique(self, log_id: str, critique_result: Dict, passed: bool, attempt: int) -> None:
        """Log critique result"""
        self.audit_db.log_critique_result(log_id, critique_result, attempt, passed)
    
    def log_safety(self, log_id: str, safety_result: Dict, passed: bool, final_output: str, action: str, reason: str = None) -> None:
        """Log safety check"""
        self.audit_db.log_safety_check(log_id, safety_result, passed, final_output, action, reason)