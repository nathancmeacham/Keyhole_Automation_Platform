# Keyhole_Automation_Platform\backend\mcp\routes\auth_me.py

from fastapi import APIRouter, Depends, Request
from backend.mcp.dependencies.auth import get_current_user, TokenData
from backend.mcp.memory.memory_singleton import memory_manager
from datetime import datetime, timezone

router = APIRouter()

@router.get("/auth/me")
async def get_me(request: Request, user: TokenData = Depends(get_current_user())):
    client_ip = request.client.host
    last_verified = memory_manager.retrieve_fact("email_verified_at", user_id=user.sub)
    ip_history = memory_manager.get_user_ips(user.sub) or []

    return {
        "email": user.sub,
        "role": user.role,
        "status": "authenticated",
        "ip": client_ip,
        "last_verified": last_verified,
        "ip_history": ip_history,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
from datetime import datetime, timezone

