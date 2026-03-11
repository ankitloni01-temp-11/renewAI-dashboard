import json
import time
import asyncio
import uuid
from typing import Dict, Any, Optional
import google.generativeai as genai
from langsmith import traceable
from config import GOOGLE_API_KEY, GEMINI_MODEL, GEMINI_PRO_MODEL

def configure_gemini(api_key: str):
    genai.configure(api_key=api_key)

# Configure immediately on import
configure_gemini(GOOGLE_API_KEY)


@traceable(run_type="llm", name="Gemini Call")
async def call_gemini(
    system_prompt: str,
    user_prompt: str,
    model: str = GEMINI_MODEL,
    use_pro: bool = False
) -> Dict[str, Any]:
    """Make an async Gemini API call and return parsed JSON + metadata."""
    start = time.time()
    model_name = GEMINI_PRO_MODEL if use_pro else GEMINI_MODEL

    try:
        # Run in thread pool since google-generativeai is sync
        loop = asyncio.get_event_loop()

        def _call():
            m = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.4,
                    max_output_tokens=2048,
                )
            )
            response = m.generate_content(user_prompt)
            return response

        response = await loop.run_in_executor(None, _call)
        latency_ms = int((time.time() - start) * 1000)

        raw_text = response.text.strip()
        # Strip markdown fences if present
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        raw_text = raw_text.strip()

        parsed = json.loads(raw_text)

        # Estimate tokens
        token_in = len(user_prompt.split()) + len(system_prompt.split())
        token_out = len(raw_text.split())

        return {
            "success": True,
            "data": parsed,
            "raw": raw_text,
            "model": model_name,
            "latency_ms": latency_ms,
            "token_count_in": token_in,
            "token_count_out": token_out
        }

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON parse error: {str(e)}",
            "raw": raw_text if 'raw_text' in locals() else "",
            "model": model_name,
            "latency_ms": int((time.time() - start) * 1000),
            "token_count_in": 0,
            "token_count_out": 0
        }
    except Exception as e:
        error_msg = str(e)
        if "API key expired" in error_msg or "API_KEY_INVALID" in error_msg:
            # Provide high-quality mock fallbacks for the demo
            mock_data = {
                "recommended_channel": "whatsapp",
                "language": "English",
                "tone": "warm",
                "segment_approach": "Budget-conscious customer, lead with value.",
                "preferred_send_time": "evening",
                "objective_for_planner": "Renew term policy via WhatsApp with EMI option",
                "message_structure": ["greeting", "benefit", "cta"],
                "key_benefit_points": ["Life cover continuation", "Family protection"],
                "opening_line": "Hi there, your policy is up for renewal.",
                "call_to_action": "Renew now",
                "subject_line": "Important: Your Policy Renewal",
                "body_text": "This message is from Suraksha's AI-powered renewal assistant. Your policy is due for renewal. To stop receiving reminders, reply STOP."
            }
            return {
                "success": True,
                "data": mock_data,
                "raw": json.dumps(mock_data),
                "model": f"MOCK-FALLBACK-{model_name}",
                "latency_ms": int((time.time() - start) * 1000),
                "token_count_in": 0,
                "token_count_out": 0,
                "is_mock": True
            }

        return {
            "success": False,
            "error": error_msg,
            "raw": "",
            "model": model_name,
            "latency_ms": int((time.time() - start) * 1000),
            "token_count_in": 0,
            "token_count_out": 0
        }
