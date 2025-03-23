# 🔒 ARCHIVED - Early prototype MCP backend with LLM-driven code suggestions
# Replaced by modular FastAPI server in backend/mcp/src/fastmcp/server.py


import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import openai

from models import FileContext, Suggestion, Approval
from permissions import is_file_allowed

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Temporary storage (ideally replace with database or persistent store)
pending_suggestions = {}

@app.get("/")
async def root():
    return {"status": "MCP Backend running"}

@app.post("/context")
async def receive_context(file_context: FileContext):
    if not is_file_allowed(file_context.filename):
        raise HTTPException(status_code=403, detail="Access to this file is forbidden.")
    
    # Call LLM API to suggest changes
    prompt = f"""
    Suggest improvements to the following code. Provide response as structured JSON:

    Filename: {file_context.filename}

    Content:
    {file_context.content}

    Provide line-specific changes and short reasoning.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    try:
        suggestion_json = response.choices[0].message.content
        suggestion = Suggestion.parse_raw(suggestion_json)
        pending_suggestions[file_context.filename] = suggestion
        return suggestion
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Response Parsing Error: {str(e)}")

@app.post("/approve")
async def approve_changes(approval: Approval):
    filename = approval.file
    if filename not in pending_suggestions:
        raise HTTPException(status_code=404, detail="No pending suggestions found for this file.")

    suggestion = pending_suggestions.pop(filename)

    if approval.approved:
        # Here you would apply changes programmatically or trigger VS Code to apply them
        # For demo purposes, we'll just acknowledge approval
        return JSONResponse(content={"status": "Changes approved and applied", "changes": suggestion.changes})
    else:
        return JSONResponse(content={"status": "Changes rejected"})

@app.get("/tools")
async def available_tools():
    # Currently static example, expand as needed
    return {"tools": ["file_editing", "code_review"], "allowed_files": list(ALLOWED_FILES)}
