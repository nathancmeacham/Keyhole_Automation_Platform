# Keyhole_Automation_Platform\tests\backend\mcp\routes\test_auth_register.py

import os
os.environ["IS_TESTING"] = "true"  # ✅ Force testing logic to activate

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.mcp.server import app
from backend.mcp.memory.memory_singleton import memory_manager

client = TestClient(app)

EMAIL = "test_user@keyholesolution.com"
PASSWORD = "SecureTest123"

# ✅ Automatically run this once per test session to reset test state
@pytest.fixture(scope="module", autouse=True)
def reset_test_user():
    try:
        memory_manager.qdrant_client.delete_collection(collection_name=f"facts_{EMAIL}")
        print(f"🧹 Deleted test collection: facts_{EMAIL}")
    except Exception as e:
        print(f"⚠️ Could not delete test collection: {e}")

# ✅ Test registration with correct patching path
@patch("backend.mcp.routes.auth_register.send_email", return_value=True)
def test_register_new_user(mock_send_email):
    response = client.post("/auth/register", json={"email": EMAIL, "password": PASSWORD})
    assert response.status_code == 200
    assert "verify" in response.json()["message"].lower()
    mock_send_email.assert_called_once()

# ✅ Ensure duplicate registrations are blocked
def test_duplicate_registration():
    response = client.post("/auth/register", json={"email": EMAIL, "password": PASSWORD})
    assert response.status_code == 409
    assert "already" in response.json()["detail"].lower()

# ✅ Password hash is stored in memory
def test_password_hash_stored():
    stored = memory_manager.retrieve_fact("password_hash", user_id=EMAIL)
    assert stored and stored.startswith("$2b$")

# ✅ Role is set to "user" by default
def test_role_assigned():
    role = memory_manager.retrieve_fact("role", user_id=EMAIL)
    assert role == "user"
