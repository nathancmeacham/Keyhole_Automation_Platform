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

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
