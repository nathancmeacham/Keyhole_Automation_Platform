# Keyhole_Automation_Platform\tests\backend\mcp\test_server.py
import pytest
from fastapi.testclient import TestClient
from backend.mcp.src.server import app

client = TestClient(app)  # ✅ Create a test client for the FastAPI app

def test_root_endpoint():
    """Test if root endpoint returns correct message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Keyhole Automation MCP Server is running!"}

def test_mcp_status():
    """Test if MCP status endpoint returns operational status."""
    response = client.get("/mcp/status")
    assert response.status_code == 200
    assert response.json() == {"status": "MCP Server is operational"}
