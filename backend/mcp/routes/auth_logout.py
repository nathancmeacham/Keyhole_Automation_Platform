# keyhole_Automation_Platform\backend\mcp\routes\auth_logout.py

from fastapi import APIRouter, Depends
from backend.mcp.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/auth/logout")
async def logout(user = Depends(get_current_user())):
    return {"message": "✅ Logged out"}
