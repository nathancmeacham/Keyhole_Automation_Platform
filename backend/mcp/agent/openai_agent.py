# Keyhole_Automation_Platform\backend\mcp\agent\openai_agent.py

import os
import re
from dotenv import load_dotenv
from fastapi import Request
from backend.mcp.memory.memory_singleton import memory_manager

load_dotenv()

ENV = os.getenv("ENV", "development").lower()
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gpt-4o")
USE_GEMINI = ENV == "development"

print(f"🔁 ENV: {ENV}")
print(f"🧠 USE_GEMINI: {USE_GEMINI}")

SYSTEM_PROMPT = (
    "You are a digital agent connected to an external memory system via an MCP backend. "
    "You can retrieve and store facts and past conversations to assist users better. "
    "Refer to memory for helpful context and continuity."
)

# Gemini setup
gemini_model = None
if USE_GEMINI:
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        gemini_model = genai.GenerativeModel("gemini-1.5-pro")
        print("✅ Gemini model loaded")
    except Exception as e:
        print("❌ Failed to initialize Gemini. Falling back to OpenAI.", e)
        USE_GEMINI = False

# OpenAI setup
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

def clean_json_string(json_str):
    return re.sub(r"^```(?:json)?|```$", "", json_str.strip(), flags=re.IGNORECASE)

def run_agent(user_message: str, model: str = None, user_id: str = "guest", client_ip: str = None) -> str:
    model_map = {
        "gpt-4o": "gpt-4o",
        "gpt-4": "gpt-4",
        "gpt-3.5-turbo": "gpt-3.5-turbo",
        "GPT-4o (Paid)": "gpt-4o",
        "ChatGPT 4 (Free)": "gpt-3.5-turbo",
        "Gemini 1.5 Pro (Free)": "gemini",
    }

    selected_model = model_map.get(model, "gemini" if USE_GEMINI else DEFAULT_LLM_MODEL)
    print(f"🧠 Requested Model: {model} → Using: {selected_model}")

    try:
        prior_memories = memory_manager.retrieve_memory(user_message, top_k=5, user_id=user_id)
    except Exception as e:
        print(f"❌ Error retrieving memory: {e}")
        prior_memories = []

    memory_snippets = (
        "\n".join([m.page_content for m in prior_memories]) if prior_memories else ""
    )

    user_name = memory_manager.retrieve_fact("name", user_id=user_id)
    print(f"🧪 Retrieved name from fact memory: {user_name}")
    known_facts = f"\nKnown facts:\n- Name: {user_name}" if user_name else ""

    system_prompt = (
        "You are a digital agent with persistent memory, connected to an external memory system via the MCP backend.\n\n"
        "You have access to two types of memory:\n"
        "- Key/Value Fact Memory: for storing exact facts like names, passwords, numbers, and user-specific data.\n"
        "- Vector Context Memory: for storing and retrieving semantically meaningful conversations and ideas.\n\n"
        "You can retrieve facts using your MCP tools. If you find a fact like the user's name, refer to it directly.\n"
        "When the user asks about their name, respond using the fact memory key 'name'. For example, if 'name = Nathan', reply: 'Your name is Nathan.\n\n"
        "If a user says, 'My name is Nathan', store 'Nathan' as their name using your fact memory system.\n\n"
        "You are not required to explain how your memory system works unless asked. Just use it naturally to be helpful."
        f"\n\nContext:\n{memory_snippets}"
        f"{known_facts}"
    )

    try:
        if selected_model == "gemini" and gemini_model:
            print("🤖 Using Gemini 1.5 Pro")
            response = gemini_model.generate_content(
                [{"role": "user", "parts": [system_prompt + f"\n\nUser: {user_message}"]}]
            )
            reply = response.text.strip()

        else:
            print(f"🤖 Using OpenAI model: {selected_model}")
            response = openai.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()

        print(f"🤖 Agent replied: {reply}")

        memory_manager.store_memory(user_message, metadata={"type": "user"}, user_id=user_id)
        memory_manager.store_memory(reply, metadata={"type": "agent"}, user_id=user_id)

        if match := re.search(r"my name is (\w+)", user_message, re.IGNORECASE):
            extracted_name = match.group(1)
            print(f"🧠 Triggered fact storage: name = {extracted_name}")
            memory_manager.store_fact("name", extracted_name, user_id=user_id)

        if user_id != "guest" and client_ip:
            print(f"🧠 Storing known IP for user {user_id}: {client_ip}")
            memory_manager.store_user_ip(user_id=user_id, ip=client_ip)

        return reply

    except Exception as e:
        print("❌ Agent error:", e)
        return "⚠️ Agent encountered an error."

# Optional FastAPI route (if running directly from this file for testing)
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AgentRequest(BaseModel):
    user_message: str
    model: str | None = None
    user_id: str | None = "guest"

@router.post("/mcp/agent")
async def agent_response(request: Request, body: AgentRequest):
    client_ip = request.client.host
    print(f"🌐 Client IP: {client_ip}")
    response = run_agent(body.user_message, model=body.model, user_id=body.user_id, client_ip=client_ip)
    return {"response": response}