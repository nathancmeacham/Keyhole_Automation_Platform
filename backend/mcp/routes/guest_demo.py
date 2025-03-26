# Keyhole_Automation_Platform\backend\mcp\routes\guest_demo.py

from fastapi import APIRouter, Depends
from backend.mcp.dependencies.auth import guest_required

router = APIRouter()

@router.get("/guest/demo")
def guest_demo(user = Depends(guest_required)):
    return {
        "message": "🧪 Welcome, guest user!",
        "tip": "You can ask general questions but must register to access saved memory.",
        "user": user.sub,
        "role": user.role
    }
