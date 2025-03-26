# Keyhole_Automation_Platform\backend\mcp\routes\admin_tools.py

from fastapi import APIRouter, Depends
from backend.mcp.dependencies.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

@router.get("/admin/dashboard")
def admin_dashboard(user=Depends(get_current_user("admin"))):
    return {
        "status": "✅ Access granted",
        "user": user.sub,
        "role": user.role
    }
