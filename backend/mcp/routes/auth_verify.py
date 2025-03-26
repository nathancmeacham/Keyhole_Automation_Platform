# Keyhole_Automation_Platform\backend\mcp\routes\auth_verify.py

from fastapi import APIRouter, HTTPException, Query, Request
from backend.mcp.utils.email_utils import confirm_email_token
from backend.mcp.memory.memory_singleton import memory_manager
from datetime import datetime

router = APIRouter()

@router.get("/auth/verify-email")
async def verify_email(request: Request, token: str = Query(...)):
    client_ip = request.client.host
    print(f"🔐 Incoming verification attempt from IP: {client_ip}")

    email = confirm_email_token(token)
    if not email:
        print("❌ Invalid or expired token used.")
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Check if user is already verified
    already_verified = memory_manager.retrieve_fact("email_verified", user_id=email)
    if already_verified == "true":
        print(f"⚠️ Email '{email}' is already verified.")
        return {
            "status": "already_verified",
            "message": f"Email '{email}' was already verified.",
            "email": email,
        }

    # Store verification flag and metadata
    memory_manager.store_fact("email_verified", "true", user_id=email)
    memory_manager.store_fact("email_verified_at", datetime.utcnow().isoformat(), user_id=email)
    memory_manager.track_user_ip(email, client_ip)

    print(f"✅ Email '{email}' successfully verified.")
    return {
        "status": "success",
        "message": "✅ Email verified successfully.",
        "email": email,
        "ip": client_ip,
        "timestamp": datetime.utcnow().isoformat(),
    }
