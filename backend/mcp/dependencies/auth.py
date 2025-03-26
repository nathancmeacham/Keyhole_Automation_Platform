# Keyhole_Automation_Platform\backend\mcp\dependencies\auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.mcp.utils.auth_utils import decode_jwt_token
from pydantic import BaseModel
from typing import Optional

# OAuth2 scheme to extract Bearer token from headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Token payload structure
class TokenData(BaseModel):
    sub: str
    role: Optional[str] = "user"

# Reusable auth dependency
def get_current_user(required_role: Optional[str] = None):
    def dependency(token: str = Depends(oauth2_scheme)) -> TokenData:
        payload = decode_jwt_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token"
            )

        try:
            user = TokenData(**payload)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Malformed token payload"
            )

        if required_role and user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Requires role '{required_role}', but you are '{user.role}'"
            )

        return user

    return dependency

# Common role-based dependencies
user_required = get_current_user(required_role="user")
admin_required = get_current_user(required_role="admin")
guest_required = get_current_user(required_role="guest")