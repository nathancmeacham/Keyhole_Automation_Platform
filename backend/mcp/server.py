# Keyhole_Automation_Platform\backend\mcp\src\server.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

load_dotenv(dotenv_path=".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# ✅ Agent endpoint
class AgentRequest(BaseModel):
    user_message: str

@app.post("/mcp/agent")
async def agent_response(request: AgentRequest):
    user_message = request.user_message
    print(f"📨 Incoming message: {user_message}")

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
        )
        agent_reply = response.choices[0].message.content
        print(f"🤖 GPT-4o replied: {agent_reply}")
        return {"response": agent_reply}

    except Exception as e:
        print("❌ Agent error:", e)
        return {"response": "⚠️ Sorry, I'm having trouble thinking right now."}

@app.get("/mcp/llm")
def llm_status():
    from backend.mcp.agent.openai_agent import USE_GEMINI, ENV, DEFAULT_LLM_MODEL
    return {
        "env": ENV,
        "llm": "gemini-1.5-pro" if USE_GEMINI else DEFAULT_LLM_MODEL
    }
