"""CRM/policy/customer data endpoints using MCP."""
from fastapi import APIRouter, Query
from typing import Optional
from mcp_client.client import mcp

router = APIRouter(prefix="/api/data", tags=["data"])

@router.get("/customers")
async def list_customers(limit: int = 50, offset: int = 0):
    # For list, we'll fetch all and slice for now
    # Data server doesn't have a 'list_customers' but we can call get_customer or similar
    # In a real app, 'data' would have a 'list' tool. 
    # For demo, we'll just mock it or add it to Data Server.
    # Let's assume Data Server can return all for simplicity in search_policies_due or similar
    policies = await mcp.call_tool("data", "search_policies_due", {"days": 365})
    return {"total": len(policies), "customers": policies[offset:offset+limit]}

@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    res = await mcp.call_tool("data", "get_customer", {"customer_id": customer_id})
    return res or {"error": "Not found"}

@router.get("/policies")
async def list_policies(limit: int = 50, offset: int = 0, product_type: Optional[str] = None, status: Optional[str] = None):
    policies = await mcp.call_tool("data", "search_policies_due", {"days": 365})
    if product_type:
        policies = [p for p in policies if p.get("product_type") == product_type]
    if status:
        policies = [p for p in policies if p.get("status") == status]
    return {"total": len(policies), "policies": policies[offset:offset+limit]}

@router.get("/policies/{policy_id}")
async def get_policy(policy_id: str):
    p = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
    if not p:
        return {"error": "Not found"}
    c = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
    return {**p, "customer": c}

@router.get("/propensity/{policy_id}")
async def get_propensity(policy_id: str):
    return await mcp.call_tool("data", "get_propensity_score", {"policy_id": policy_id})

@router.get("/objections")
async def list_objections():
    # Knowledge server search with empty query as a hack for list
    res = await mcp.call_tool("knowledge", "search_objections", {"query": "", "n": 100})
    return {"total": len(res.get("results", [])), "objections": res.get("results", [])}

@router.get("/objections/search")
async def search_objections(q: str = ""):
    res = await mcp.call_tool("knowledge", "search_objections", {"query": q, "n": 10})
    return {"results": res.get("results", [])}

@router.get("/team")
async def get_team():
    res = await mcp.call_tool("data", "get_team_status", {})
    return {"team": res}

@router.get("/compliance-rules")
async def get_compliance_rules():
    res = await mcp.call_tool("knowledge", "get_compliance_rules", {})
    return res
