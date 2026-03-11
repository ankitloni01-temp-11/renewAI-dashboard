from fastapi import APIRouter, Request, HTTPException
from mcp_client.client import mcp
import logging

router = APIRouter(prefix="/api/elevenlabs", tags=["elevenlabs"])
logger = logging.getLogger(__name__)

@router.post("/webhook")
async def elevenlabs_webhook(request: Request):
    """
    Handle tool calls from ElevenLabs Conversational AI.
    ElevenLabs sends a POST request with the tool name and arguments.
    """
    data = await request.json()
    logger.info(f"ElevenLabs Webhook received: {data}")
    
    # ElevenLabs Webhook Schema:
    # {
    #   "tool_name": "get_policy_details",
    #   "args": { "policy_id": "SLI-123" }
    # }
    
    tool_name = data.get("tool_name")
    args = data.get("args", {})
    
    try:
        if tool_name == "get_policy_details":
            policy_id = args.get("policy_id")
            if not policy_id:
                return {"error": "policy_id is required"}
            
            policy = await mcp.call_tool("data", "get_policy", {"policy_id": policy_id})
            customer = await mcp.call_tool("data", "get_customer_by_policy", {"policy_id": policy_id})
            
            return {
                "policy_info": policy,
                "customer_info": customer
            }
            
        elif tool_name == "check_renewal_status":
            policy_id = args.get("policy_id")
            if not policy_id:
                return {"error": "policy_id is required"}
            
            journey = await mcp.call_tool("data", "get_journey_state", {"policy_id": policy_id})
            return {"status": journey.get("status", "unknown"), "details": journey}
            
        elif tool_name == "simulate_payment":
            policy_id = args.get("policy_id")
            if not policy_id:
                return {"error": "policy_id is required"}
            
            result = await mcp.call_tool("data", "mark_payment", {"policy_id": policy_id})
            return {"success": True, "message": f"Payment marked for {policy_id}", "result": result}
            
        else:
            return {"error": f"Unknown tool: {tool_name}"}
            
    except Exception as e:
        logger.error(f"Error in ElevenLabs Webhook: {e}")
        return {"error": str(e)}
