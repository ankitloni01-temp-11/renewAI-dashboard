"""Mock external service endpoints using MCP."""
from fastapi import APIRouter
from typing import Dict, Any
import uuid, random
from mcp_client.client import mcp
from datetime import datetime

router = APIRouter(prefix="/api/mock", tags=["mock"])

@router.post("/sendgrid/send")
async def mock_sendgrid_send(payload: Dict[str, Any]):
    msg_id = f"sendgrid_{uuid.uuid4().hex[:12]}"
    return {"message_id": msg_id, "status": "queued"}

@router.post("/gupshup/send")
async def mock_gupshup_send(payload: Dict[str, Any]):
    return {"message_id": f"wa_{uuid.uuid4().hex[:10]}", "status": "sent"}

@router.post("/exotel/call")
async def mock_exotel_call(payload: Dict[str, Any]):
    return {"call_id": f"call_{uuid.uuid4().hex[:10]}", "status": "initiated"}

@router.post("/razorpay/pay")
async def mock_razorpay_pay(policy_id: str, amount: int):
    payment_id = f"pay_{uuid.uuid4().hex[:12]}"
    await mcp.call_tool("data", "mark_payment", {"policy_id": policy_id})
    return {"payment_id": payment_id, "status": "captured"}

@router.post("/dlp/inspect")
async def mock_dlp_inspect(payload: Dict[str, Any]):
    """Mock PII scanning using MCP Safety Server."""
    text = payload.get("text", "")
    result = await mcp.call_tool("safety", "scan_pii", {"text": text})
    return result
