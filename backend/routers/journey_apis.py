"""Journey state APIs using MCP."""
from fastapi import APIRouter, BackgroundTasks
from typing import Optional
from mcp_client.client import mcp
from graph.renewal_graph import run_renewal_journey

router = APIRouter(prefix="/api/journeys", tags=["journeys"])

@router.get("")
async def list_journeys(status: Optional[str] = None):
    # In demo, we get all from Data Server
    # Note: We need a 'list_journeys' equivalent or assume we get all
    return await mcp.call_tool("data", "get_journey_state", {"policy_id": None})

@router.get("/{policy_id}")
async def get_journey(policy_id: str):
    j = await mcp.call_tool("data", "get_journey_state", {"policy_id": policy_id})
    if not j:
        return {"error": "Journey not found"}
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    return {**j, "policy": policy, "customer": customer}

@router.post("/{policy_id}/start")
async def start_journey(policy_id: str, background_tasks: BackgroundTasks):
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    if not policy:
        return {"error": "Policy not found"}
    background_tasks.add_task(run_renewal_journey, policy_id)
    return {"message": f"Journey started for {policy_id}", "policy_id": policy_id}
