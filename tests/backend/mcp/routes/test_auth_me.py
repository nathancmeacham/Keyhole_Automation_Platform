# Keyhole_Automation_Platform\tests\backend\mcp\routes\test_auth_me.py

import os
os.environ["IS_TESTING"] = "true"

import pytest
from fastapi.testclient import TestClient
from backend.mcp.server import app
from backend.mcp.utils.auth_utils import create_jwt_token

client = TestClient(app)

EMAIL = "test_user@keyholesolution.com"
ROLE = "user"

# ✅ Valid JWT created for testing
VALID_TOKEN = create_jwt_token({"sub": EMAIL, "role": ROLE})
INVALID_TOKEN = "this.is.not.valid"

headers_with_valid_token = {"Authorization": f"Bearer {VALID_TOKEN}"}
headers_with_invalid_token = {"Authorization": f"Bearer {INVALID_TOKEN}"}


def test_me_valid_token():
    response = client.get("/auth/me", headers=headers_with_valid_token)
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == EMAIL
    assert body["role"] == ROLE
    assert body["status"] == "authenticated"


def test_me_missing_token():
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_me_invalid_token():
    response = client.get("/auth/me", headers=headers_with_invalid_token)
    assert response.status_code == 401
    assert "Invalid or missing token" in response.json()["detail"]
