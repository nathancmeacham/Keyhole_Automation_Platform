# Keyhole_Automation_Platform\backend\mcp\agent\openai_agent.py

import os
from dotenv import load_dotenv
load_dotenv()

ENV = os.getenv("ENV", "development").lower()
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gpt-4o")

USE_GEMINI = ENV == "development"

print(f"🔁 ENV: {ENV}")
print(f"🧠 USE_GEMINI: {USE_GEMINI}")

# Try Gemini setup
gemini_model = None
if USE_GEMINI:
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        gemini_model = genai.GenerativeModel("gemini-1.5-pro")
        print("✅ Gemini model loaded")
    except Exception as e:
        print("❌ Failed to initialize Gemini. Falling back to OpenAI.")
        USE_GEMINI = False

# OpenAI setup (fallback or production)
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Memory system
from backend.mcp.memory.memory_manager import store_memory, retrieve_memory

def run_agent(user_message: str, model: str = None) -> str:
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

    # 🔍 Retrieve memory for context
    prior_memories = retrieve_memory(user_message, top_k=5)
    memory_snippets = "\n".join([m.page_content for m in prior_memories]) if prior_memories else ""

    system_prompt = (
        "You are a helpful assistant. Refer to past user queries to maintain continuity.\n"
        f"Relevant context from memory:\n{memory_snippets}\n"
    )

    try:
        if selected_model == "gemini" and gemini_model:
            print("🤖 Using Gemini 1.5 Pro")
            response = gemini_model.generate_content(f"{system_prompt}\nUser: {user_message}")
            reply = response.text.strip()
        else:
            print(f"🤖 Using OpenAI model: {selected_model}")
            response = openai.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()

        # 💾 Store interaction
        store_memory(user_message, metadata={"type": "user"})
        store_memory(reply, metadata={"type": "agent"})

        return reply

    except Exception as e:
        print("❌ Agent error:", e)
        return "⚠️ Agent encountered an error."