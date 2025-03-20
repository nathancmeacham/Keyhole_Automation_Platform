# Keyhole_Automation_Platform\backend\mcp\src\server.py
from fastapi import FastAPI
import backend.mcp.controllers.mcp_controller as controller  # ✅ Import module, not just mcp_router

app = FastAPI()
app.include_router(controller.mcp_router, prefix="/mcp")  # ✅ Reference the module attribute

@app.get("/")
async def root():
    return {"message": "Keyhole Automation MCP Server is running!"}
