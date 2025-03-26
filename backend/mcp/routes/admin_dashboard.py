# Keyhole_Automation_Platform\backend\mcp\routes\admin_dashboard.py

from fastapi import APIRouter, Depends
from backend.mcp.dependencies.auth import admin_required

router = APIRouter()

@router.get("/admin/stats")
def admin_stats(user = Depends(admin_required)):
    return {"message": f"Welcome admin {user.sub}", "role": user.role}
