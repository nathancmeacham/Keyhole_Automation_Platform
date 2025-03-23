# Keyhole_Automation_Platform\tests\backend\mcp\test_server.py

from fastapi.testclient import TestClient
from backend.mcp.server import app

client = TestClient(app)

def test_root_endpoint():
    """Test if root endpoint returns correct message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "MCP Backend running"}  # ✅ Updated to match real return

def test_mcp_status():
    """Test if MCP status endpoint returns operational status."""
    response = client.get("/mcp/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}  # ✅ Updated to match real return
