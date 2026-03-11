from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from mcp_client.client import mcp

router = APIRouter(prefix="/api/test/mcp", tags=["test_mcp"])

@router.post("/{server_name}/{tool_name}")
async def call_mcp_tool(server_name: str, tool_name: str, arguments: Optional[Dict[str, Any]] = None):
    """
    Temporary endpoint to call any MCP tool directly for testing.
    Args:
        server_name (str): The name of the MCP server (data, knowledge, or safety).
        tool_name (str): The name of the tool to call.
        arguments (Dict, optional): The arguments to pass to the tool.
    Returns:
        The raw result from the MCP tool call.
    """
    try:
        result = await mcp.call_tool(server_name, tool_name, arguments or {})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simplified specific routes to match the curl commands in the testing plan
@router.get("/{server_name}/{tool_name}")
async def call_mcp_tool_get(server_name: str, tool_name: str, customer_id: Optional[str] = None, policy_id: Optional[str] = None):
    """Support GET for simplicity if needed by some curl commands without -d."""
    args = {}
    if customer_id: args["customer_id"] = customer_id
    if policy_id: args["policy_id"] = policy_id
    
    return await call_mcp_tool(server_name, tool_name, args)
