"""Human queue CRUD APIs using MCP."""
from fastapi import APIRouter
from typing import Optional
from mcp_client.client import mcp
from datetime import datetime

router = APIRouter(prefix="/api/human-queue", tags=["human-queue"])

@router.get("")
async def list_queue(priority: Optional[str] = None, status: Optional[str] = None):
    cases = await mcp.call_tool("data", "get_queue", {})
    if priority:
        cases = [c for c in cases if c.get("priority") == priority]
    if status:
        cases = [c for c in cases if c.get("status") == status]
    return {"total": len(cases), "cases": cases}

@router.get("/{case_id}")
async def get_case(case_id: str):
    # Data server uses policy_id as key for human_queue for simplicity in this demo
    # In a real app, case_id lookup would be separate.
    # For now, we assume case_id is passed as policy_id or we filter.
    cases = await mcp.call_tool("data", "get_queue", {})
    case = next((c for c in cases if c.get("case_id") == case_id), None)
    if not case:
        return {"error": "Case not found"}
    
    policy_id = case.get("policy_id")
    policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    audit = await mcp.call_tool("data", "get_audit_trail", {"policy_id": policy_id})
    return {**case, "policy": policy, "customer": customer, "audit_trail": audit}

@router.put("/{case_id}/assign")
async def assign_case(case_id: str, assigned_to: str):
    cases = await mcp.call_tool("data", "get_queue", {})
    case = next((c for c in cases if c.get("case_id") == case_id), None)
    if not case:
        return {"error": "Not found"}
    
    await mcp.call_tool("data", "assign_case", {"policy_id": case["policy_id"], "member_id": assigned_to})
    case["assigned_to"] = assigned_to
    case["status"] = "assigned"
    return case

@router.put("/{case_id}/resolve")
async def resolve_case(case_id: str, resolution: str, notes: str = "", resolved_by: str = ""):
    cases = await mcp.call_tool("data", "get_queue", {})
    case = next((c for c in cases if c.get("case_id") == case_id), None)
    if not case:
        return {"error": "Not found"}

    policy_id = case["policy_id"]
    await mcp.call_tool("data", "resolve_case", {"policy_id": policy_id})
    
    # Update journey
    journey_status = "paid" if "paid" in resolution.lower() or "renewed" in resolution.lower() else "resolved"
    await mcp.call_tool("data", "update_journey_state", {"policy_id": policy_id, "updates": {"status": journey_status}})
    
    return {"status": "success", "case_id": case_id}
