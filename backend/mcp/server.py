# Keyhole_Automation_Platform\backend\mcp\server.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.mcp.agent.openai_agent import run_agent, USE_GEMINI, ENV, DEFAULT_LLM_MODEL

load_dotenv(dotenv_path=".env")

app = FastAPI()

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
