# Keyhole_Automation_Platform\backend\mcp\server.py

import os
from fastapi import FastAPI, HTTPException, Depends
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

@app.post("/mcp/agent")
async def agent_response(request: AgentRequest):
    print(f"📨 Incoming message: {request.user_message}")
    print(f"🔁 Requested model: {request.model}")

    try:
        response = run_agent(request.user_message, model=request.model)
        print(f"🤖 Agent replied: {response}")
        return {"response": response}

    except Exception as e:
        print("❌ Agent error:", e)
        return {"response": "⚠️ Sorry, I'm having trouble thinking right now."}

# ✅ Memory endpoints
class MemoryRequest(BaseModel):
    text: str
    metadata: dict

@app.post("/mcp/memory/store")
async def store_memory(request: MemoryRequest):
    try:
        memory_manager.store_memory(request.text, request.metadata)
        return {"status": "Memory stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/memory/retrieve")
async def retrieve_memory(request: MemoryRequest):
    try:
        results = memory_manager.retrieve_memory(request.text, request.metadata.get("type"))
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
