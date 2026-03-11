import pytest
import os
from agents.orchestrator import run_orchestrator
from agents.planner import run_planner
from agents.email_agent import run_email_agent

@pytest.mark.asyncio
async def test_orchestrator_rajesh(mcp):
    """Rajesh: WhatsApp-first, term policy"""
    result = await run_orchestrator(policy_id="SLI-2298741")
    
    assert "recommended_channel" in result
    assert result["recommended_channel"] in ["whatsapp", "email", "voice"]
    assert "language" in result
    assert "objective_for_planner" in result
    assert "key_value_propositions" in result
    assert isinstance(result["key_value_propositions"], list)

@pytest.mark.asyncio
async def test_planner_rajesh(mcp):
    """Planner: Create execution plan for Rajesh"""
    orch_result = {
        "recommended_channel": "whatsapp",
        "language": "Hindi",
        "tone": "warm",
        "segment_approach": "Emphasize family protection and flexible payment",
        "objective_for_planner": "Send renewal reminder for Term Shield due March 15",
        "key_value_propositions": ["Life cover continuation", "Family protection"]
    }
    result = await run_planner(policy_id="SLI-2298741", orchestrator_result=orch_result)
    
    assert "message_structure" in result
    assert "key_benefit_points" in result
    assert "payment_options_to_offer" in result
    
    # Flexible check for opening_line or message_structure content
    if "opening_line" in result:
        assert isinstance(result["opening_line"], str)
    else:
        assert isinstance(result["message_structure"], (dict, list))
        assert len(result["message_structure"]) > 0

@pytest.mark.asyncio
async def test_email_agent_vikram(mcp):
    """Email Agent: Generate email for Rajesh (demoing tool use)"""
    orch_result = {
        "recommended_channel": "email",
        "language": "English",
        "tone": "professional",
        "objective_for_planner": "Renewal for Term Shield",
        "key_value_propositions": ["Protection"]
    }
    plan = {
        "message_structure": {"opening": "Hello"},
        "key_benefit_points": ["Term insurance"],
        "opening_line": "Hi Rajesh,",
        "call_to_action": "Renew link"
    }
    
    result = await run_email_agent(policy_id="SLI-2298741", plan=plan, orch_result=orch_result)
    
    assert "subject_line" in result
    assert "body_text" in result
    # Ground truth check from seed data/MCP
    assert "24,000" in result["body_text"] or "24000" in result["body_text"]
