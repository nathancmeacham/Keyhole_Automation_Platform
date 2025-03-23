# Keyhole_Automation_Platform\backend\mcp\src\routes.py
from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/status")
async def get_status():
    return {"status": "MCP Server operational"}
