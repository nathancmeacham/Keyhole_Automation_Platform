# Keyhole_Automation_Platform\backend\mcp\routes\auth_login.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from backend.mcp.utils.auth_utils import verify_password, create_jwt_token
from backend.mcp.memory.memory_singleton import memory_manager

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str

@router.post("/auth/login", response_model=LoginResponse)
async def login_user(request: LoginRequest):
    email = request.email.lower().strip()
    password = request.password

    # 🔐 Retrieve password hash
    stored_hash = memory_manager.retrieve_fact("password_hash", user_id=email)
    if not stored_hash:
        print("❌ No password hash found.")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 🔐 Verify password
    if not verify_password(password, stored_hash):
        print("❌ Password mismatch.")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # ✅ Check email verification
    verified = memory_manager.retrieve_fact("email_verified", user_id=email)
    if verified != "true":
        print("⚠️ Email not verified.")
        raise HTTPException(status_code=403, detail="Email is not verified")

    # 🎟️ Issue token
    token = create_jwt_token({"sub": email, "role": "user"})

    print(f"✅ Login success for {email}")
    return LoginResponse(access_token=token, email=email)
