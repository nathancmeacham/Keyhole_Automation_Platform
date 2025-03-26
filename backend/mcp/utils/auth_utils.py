# Keyhole_Automation_Platform\backend\mcp\utils\auth_utils.py

import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# 🔐 Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_IN_MINUTES = int(os.getenv("JWT_EXPIRES_IN_MINUTES", 60 * 24))  # default: 1 day

# ✉️ Email token configuration
EMAIL_TOKEN_SECRET = os.getenv("EMAIL_TOKEN_SECRET", "email_secret")
EMAIL_TOKEN_EXPIRES_MINUTES = int(os.getenv("EMAIL_TOKEN_EXPIRES_MINUTES", 60 * 24))  # default: 24 hrs


# 🔐 Password utilities
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 🎟️ JWT utilities
def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=JWT_EXPIRES_IN_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        print(f"❌ Failed to decode JWT: {e}")
        return None


# ✉️ Email verification token utilities
def create_email_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=EMAIL_TOKEN_EXPIRES_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, EMAIL_TOKEN_SECRET, algorithm=JWT_ALGORITHM)

def confirm_email_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, EMAIL_TOKEN_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError as e:
        print(f"❌ Invalid email token: {e}")
        return None
