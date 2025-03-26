# Keyhole_Automation_Platform\tests\backend\mcp\routes\test_auth_verify.py

import os
os.environ["IS_TESTING"] = "true"

import pytest
from fastapi.testclient import TestClient
from backend.mcp.server import app
from backend.mcp.memory.memory_singleton import memory_manager
from backend.mcp.utils.email_utils import generate_email_token

client = TestClient(app)

EMAIL = "test_user@keyholesolution.com"

# ✅ Ensure token verification works
def test_valid_token_verification():
    token = generate_email_token(EMAIL)
    response = client.get(f"/auth/verify-email?token={token}")
    assert response.status_code == 200
    assert "verified" in response.json()["message"].lower()

# ✅ Ensure invalid tokens are rejected
def test_invalid_token():
    response = client.get("/auth/verify-email?token=badtoken123")
    assert response.status_code == 400
    assert "invalid" in response.json()["detail"].lower()

# ✅ Ensure email_verified fact is set
def test_email_verified_fact():
    verified = memory_manager.retrieve_fact("email_verified", user_id=EMAIL)
    assert str(verified).lower() == "true"