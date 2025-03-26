# Keyhole_Automation_Platform\backend\mcp\routes\auth_register.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from backend.mcp.utils.auth_utils import hash_password
from backend.mcp.utils.email_utils import generate_email_token, send_email
from backend.mcp.memory.memory_singleton import memory_manager

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/auth/register")
async def register_user(request: RegisterRequest):
    email = request.email.lower()
    user_id = email  # for clarity and consistency

    # 🔍 Check if user already exists (avoid matching on string "None")
    existing_hash = memory_manager.retrieve_fact("password_hash", user_id=user_id)
    if existing_hash is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    # 🔐 Store hashed password and default role
    hashed_pw = hash_password(request.password)
    memory_manager.store_fact("password_hash", hashed_pw, user_id=user_id)
    memory_manager.store_fact("role", "user", user_id=user_id)

    # ✉️ Prepare email content
    token = generate_email_token(user_id)
    verification_link = f"http://localhost:8000/auth/verify-email?token={token}"
    subject = "✅ Verify your email"
    body = f"Welcome to Keyhole!\n\nClick below to verify your account:\n\n{verification_link}"

    # ✉️ Attempt to send email
    if send_email(user_id, subject, body):
        return {"message": "✅ Registration successful. Please verify your email."}
    else:
        raise HTTPException(status_code=500, detail="Failed to send verification email")
