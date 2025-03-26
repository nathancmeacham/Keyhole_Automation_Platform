# Keyhole_Automation_Platform\backend\mcp\server.py

import os
from fastapi import Query
from backend.mcp.utils.email_utils import send_email
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.mcp.agent.openai_agent import run_agent, USE_GEMINI, ENV, DEFAULT_LLM_MODEL
from backend.mcp.tools import oracle_apex_tool
from backend.mcp.memory.memory_singleton import memory_manager

load_dotenv(dotenv_path=".env")

app = FastAPI()
app.include_router(oracle_apex_tool.router)

# ✅ CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check: root
@app.get("/")
def root():
    return {"status": "MCP Backend running"}

# ✅ Health check: status
@app.get("/mcp/status")
def mcp_status():
    return {"status": "ok"}

# ✅ LLM info endpoint
@app.get("/mcp/llm")
def llm_status():
    return {
        "env": ENV,
        "llm": "gemini-1.5-pro" if USE_GEMINI else DEFAULT_LLM_MODEL
    }

@app.get("/routes")
def list_routes():
    return [route.path for route in app.routes]

# ✅ Agent endpoint
class AgentRequest(BaseModel):
    user_message: str
    model: str | None = None  # ✅ optional model override from frontend
    user_id: str | None = "guest"  # ✅ user ID passed from frontend, default to 'guest'

@app.post("/mcp/agent")
async def agent_response(request: Request, body: AgentRequest):
    client_ip = request.client.host
    print(f"🌐 Client IP: {client_ip}")

    if body.user_id == "guest":
        memory_manager.store_guest_ip(client_ip)

    print(f"📨 Incoming message: {body.user_message}")
    print(f"🔁 Requested model: {body.model}")
    print(f"👤 User ID: {body.user_id}")

    try:
        response = run_agent(body.user_message, model=body.model, user_id=body.user_id)
        print(f"🤖 Agent replied: {response}")
        return {"response": response}

    except Exception as e:
        print("❌ Agent error:", e)
        return {"response": "⚠️ Sorry, I'm having trouble thinking right now."}

# ✅ Memory endpoints
class MemoryRequest(BaseModel):
    text: str
    metadata: dict
    user_id: str | None = "guest"

@app.post("/mcp/memory/store")
async def store_memory(request: MemoryRequest):
    try:
        memory_manager.store_memory(request.text, request.metadata, user_id=request.user_id)
        return {"status": "Memory stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/memory/retrieve")
async def retrieve_memory(request: MemoryRequest):
    try:
        results = memory_manager.retrieve_memory(request.text, request.metadata.get("type"), user_id=request.user_id)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# ✅ Email endpoint
@app.get("/test-email")
def test_email(to: str = Query(..., description="Target email address")):
    subject = "🔐 Test Email from Keyhole MCP"
    body = "This is a test message sent from the Keyhole MCP server."
    result = send_email(to, subject, body)
    return {"sent": result}