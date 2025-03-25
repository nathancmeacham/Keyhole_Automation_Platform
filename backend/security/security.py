# Keyhole_Automation_Platform\backend\mcp\security.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Placeholder: Implement actual token verification logic here
    if token == "valid-token":
        return User(user_id=1, username="Nathan")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
