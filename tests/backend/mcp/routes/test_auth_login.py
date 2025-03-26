# Keyhole_Automation_Platform\tests\backend\mcp\routes\test_auth_me.py

import os
os.environ["IS_TESTING"] = "true"

import pytest
from fastapi.testclient import TestClient
from backend.mcp.server import app
from backend.mcp.utils.auth_utils import create_jwt_token

client = TestClient(app)

EMAIL = "test_user@keyholesolution.com"
VALID_TOKEN = create_jwt_token({"sub": EMAIL, "role": "user"})
INVALID_TOKEN = "this.is.not.valid"

def test_me_valid_token():
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == EMAIL
    assert data["role"] == "user"
    assert data["status"] == "authenticated"

def test_me_missing_token():
    response = client.get("/auth/me")
    assert response.status_code == 401

def test_me_invalid_token():
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {INVALID_TOKEN}"}
    )
    assert response.status_code == 401
