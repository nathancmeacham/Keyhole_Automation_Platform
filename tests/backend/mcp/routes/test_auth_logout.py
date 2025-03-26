# Keyhole_Automation_Platform\tests\backend\mcp\routes\test_auth_logout.py

import os
os.environ["IS_TESTING"] = "true"  # ✅ Ensure testing mode is active

import pytest
from fastapi.testclient import TestClient
from backend.mcp.server import app
from backend.mcp.utils.auth_utils import create_jwt_token

client = TestClient(app)

EMAIL = "test_user@keyholesolution.com"

# ✅ Generate a valid token manually for logout test
VALID_TOKEN = create_jwt_token({"sub": EMAIL, "role": "user"})
INVALID_TOKEN = "this.is.not.a.valid.token"

# ✅ Successful logout should return 200
def test_logout_with_valid_token():
    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {VALID_TOKEN}"})
    assert response.status_code == 200
    assert response.json()["message"].lower() == "✅ logged out"


# ✅ Missing token should return 401
def test_logout_missing_token():
    response = client.post("/auth/logout")
    assert response.status_code == 401
    assert "not authenticated" in response.json()["detail"].lower()

# ✅ Invalid token should return 401
def test_logout_invalid_token():
    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {INVALID_TOKEN}"})
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()
