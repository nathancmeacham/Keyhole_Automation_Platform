from fastapi import APIRouter

mcp_router = APIRouter()  # ✅ Ensure this is correctly defined

@mcp_router.get("/status")
async def mcp_status():
    return {"status": "MCP Server is operational"}
