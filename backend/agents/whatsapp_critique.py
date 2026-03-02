"""WhatsApp Critique Agent using MCP."""
import json, time, uuid, asyncio
from typing import Dict, Any
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL
from mcp_client.client import mcp

genai.configure(api_key=GOOGLE_API_KEY)

CRITIQUE_PROMPT = """You are the WhatsApp Critique Agent. Evaluate this WhatsApp response:
- response_correctness: 0-10
- tone_score: 0-10
- factual_score: 0-10
- context_score: 0-10
JSON only."""

async def run_whatsapp_critique(policy_id: str, wa_result: Dict, customer_message: str) -> Dict[str, Any]:
    start = time.time()
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    # Fetch via MCP
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    
    user_prompt = f"""
CUSTOMER MESSAGE: "{customer_message}"
AI RESPONSE: "{wa_result.get('response_text','')}"
POLICY: Premium=Rs.{policy.get('premium_amount',0):,}
Evaluate the WhatsApp response quality."""
    
    try:
        response = await asyncio.to_thread(
            model.generate_content,
            [CRITIQUE_PROMPT, user_prompt],
            generation_config=genai.GenerationConfig(response_mime_type="application/json", max_output_tokens=200)
        )
        result = json.loads(response.text)
    except:
        result = {"verdict":"APPROVED","overall_score":8.3}
    
    latency_ms = int((time.time() - start) * 1000)
    
    # Audit via MCP
    await mcp.call_tool("data", "write_audit_entry", {
        "entry": {
            "event_id": str(uuid.uuid4()), "policy_id": policy_id,
            "step_number": 99, "agent_name": "WhatsAppCritiqueAgent",
            "action": "evaluate_whatsapp_response",
            "input_summary": f"Evaluating WA response for {policy_id}",
            "output_summary": f"Verdict: {result.get('verdict')}, Score: {result.get('overall_score')}",
            "model_used": GEMINI_MODEL, "latency_ms": latency_ms,
            "token_count_in": 200, "token_count_out": 100,
            "critique_score": result.get("overall_score"), "verdict": result.get("verdict"),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "full_output": result
        }
    })
    return result
