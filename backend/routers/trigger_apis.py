"""Trigger APIs using MCP."""
from fastapi import APIRouter, BackgroundTasks
from typing import Optional
import random
from mcp_client.client import mcp
from graph.renewal_graph import run_renewal_journey
from datetime import datetime
import asyncio

router = APIRouter(prefix="/api/triggers", tags=["triggers"])

async def _start_with_delay(policy_id: str, delay: float):
    await asyncio.sleep(delay)
    await run_renewal_journey(policy_id)

@router.post("/t45-scan")
async def t45_scan(background_tasks: BackgroundTasks, count: int = 5):
    """Pick N policies without active journeys and start their journeys."""
    policies = await mcp.call_tool("data", "search_policies_due", {"days": 365})
    candidates = []
    for p in policies:
        pid = p.get("policy_id")
        journey = await mcp.call_tool("data", "get_journey_state", {"policy_id": pid})
        if not journey or journey.get("status") in ["not_started", "None"]:
            candidates.append(pid)
    
    selected = random.sample(candidates, min(count, len(candidates)))
    for i, policy_id in enumerate(selected):
        delay = i * 2.0
        background_tasks.add_task(_start_with_delay, policy_id, delay)
    
    return {"triggered": len(selected), "policy_ids": selected}

@router.post("/single/{policy_id}")
async def start_single_journey(policy_id: str, background_tasks: BackgroundTasks):
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    if not policy:
        return {"error": "Policy not found"}
    
    # Reset via MCP
    await mcp.call_tool("data", "update_journey_state", {
        "policy_id": policy_id, 
        "updates": {"status": "not_started", "paid_at": None, "current_step": "init"}
    })
    
    background_tasks.add_task(run_renewal_journey, policy_id)
    return {"message": f"Journey started for {policy_id}", "policy_id": policy_id}

@router.post("/simulate-payment/{policy_id}")
async def simulate_payment(policy_id: str):
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    if not policy:
        return {"error": "Policy not found"}
    
    await mcp.call_tool("data", "mark_payment", {"policy_id": policy_id})
    
    return {
        "success": True,
        "policy_id": policy_id,
        "message": f"Payment simulated for {policy_id}"
    }

@router.post("/reset-demo")
async def reset_demo():
    """Reset demo via MCP."""
    demo_pids = ["SLI-2298741", "SLI-882341", "SLI-445678"]
    for pid in demo_pids:
        await mcp.call_tool("data", "update_journey_state", {
            "policy_id": pid, 
            "updates": {"status": "not_started", "paid_at": None, "current_step": "init"}
        })
    return {"message": "Demo reset complete."}
