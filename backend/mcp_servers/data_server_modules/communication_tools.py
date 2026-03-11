"""Communication tool handlers with real SMTP and Twilio integrations."""
import uuid
import time
import os
import asyncio
from typing import Dict, Any, List
from email.message import EmailMessage
import aiosmtplib
from twilio.rest import Client
from . import shared_state as state

# Load credentials from env
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

async def send_email(arguments: Dict) -> Dict:
    msg_id = f"MSG-{str(uuid.uuid4())[:8].upper()}"
    recipient = arguments.get("to")
    subject = arguments.get("subject")
    body = arguments.get("body")

    # Store in state (mock audit)
    state.messages[msg_id] = {
        "id": msg_id,
        "channel": "email",
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "status": "pending",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    if not all([SMTP_USER, SMTP_PASSWORD]):
        print(f"DEBUG: SMTP credentials missing. Mocking email to {recipient}")
        state.messages[msg_id]["status"] = "mock_sent"
        return {"status": "success", "message_id": msg_id, "mode": "mock"}

    try:
        message = EmailMessage()
        message["From"] = SMTP_USER
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True if SMTP_PORT == 587 else False
        )
        state.messages[msg_id]["status"] = "sent"
        return {"status": "success", "message_id": msg_id}
    except Exception as e:
        state.messages[msg_id]["status"] = "failed"
        state.messages[msg_id]["error"] = str(e)
        return {"status": "error", "error": str(e)}

async def send_whatsapp(arguments: Dict) -> Dict:
    msg_id = f"MSG-{str(uuid.uuid4())[:8].upper()}"
    recipient = arguments.get("to")
    body = arguments.get("body")

    # Ensure recipient starts with whatsapp:
    if not recipient.startswith("whatsapp:"):
        recipient = f"whatsapp:{recipient}"

    state.messages[msg_id] = {
        "id": msg_id,
        "channel": "whatsapp",
        "recipient": recipient,
        "body": body,
        "status": "pending",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    if not all([TWILIO_SID, TWILIO_TOKEN]):
        print(f"DEBUG: Twilio credentials missing. Mocking WhatsApp to {recipient}")
        state.messages[msg_id]["status"] = "mock_delivered"
        return {"status": "success", "message_id": msg_id, "mode": "mock"}

    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=body,
            to=recipient
        )
        state.messages[msg_id]["status"] = "delivered"
        state.messages[msg_id]["twilio_sid"] = message.sid
        return {"status": "success", "message_id": msg_id}
    except Exception as e:
        state.messages[msg_id]["status"] = "failed"
        state.messages[msg_id]["error"] = str(e)
        return {"status": "error", "error": str(e)}

def initiate_voice_call(arguments: Dict) -> Dict:
    # Voice is handled by ElevenLabs in the frontend simulator
    # This tool remains for journey logic consistency
    msg_id = f"MSG-{str(uuid.uuid4())[:8].upper()}"
    state.messages[msg_id] = {
        "id": msg_id,
        "channel": "voice",
        "recipient": arguments.get("to"),
        "status": "session_init",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    return {"status": "success", "message_id": msg_id}

def get_message_status(arguments: Dict) -> Dict:
    msg_id = arguments.get("message_id")
    return state.messages.get(msg_id, {"status": "not_found"})

def get_channel_stats(arguments: Dict) -> Dict:
    stats = {"email": 0, "whatsapp": 0, "voice": 0}
    for m in state.messages.values():
        c = m.get("channel")
        if c in stats:
            stats[c] += 1
    return stats
