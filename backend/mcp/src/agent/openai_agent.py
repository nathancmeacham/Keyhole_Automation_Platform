# Keyhole_Automation_Platform\backend\mcp\src\agent\openai_agent.py

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()  # 🔑 Load from root .env

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def run_agent_logic(user_message: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a facility management company."},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Agent error: {e}"
