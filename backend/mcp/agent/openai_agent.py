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


def run_agent(user_message: str) -> str:
    try:
        if USE_GEMINI and gemini_model:
            print("🤖 Using Gemini 1.5 Pro")
            response = gemini_model.generate_content(user_message)
            return response.text.strip()

        print(f"🤖 Using OpenAI model: {DEFAULT_LLM_MODEL}")
        response = openai.chat.completions.create(
            model=DEFAULT_LLM_MODEL,
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ Agent error:", e)
        return "⚠️ Agent encountered an error."
