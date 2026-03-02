"""Audit trail endpoints using MCP."""
from fastapi import APIRouter
from mcp_client.client import mcp

router = APIRouter(prefix="/api/audit", tags=["audit"])

@router.get("/{policy_id}")
async def get_audit_trail(policy_id: str):
    """Get audit trail for a policy via MCP Data Server."""
    return await mcp.call_tool("data", "get_audit_trail", {"policy_id": policy_id})

@router.get("/")
async def list_all_audit():
    """Get full audit trail via MCP Data Server."""
    return await mcp.call_tool("data", "get_audit_trail", {})
