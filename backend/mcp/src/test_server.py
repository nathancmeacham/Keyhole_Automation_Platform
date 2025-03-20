# Keyhole_Automation_Platform\backend\mcp\tests\test_server.py
import pytest
from httpx import AsyncClient
from src.server import app

@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Keyhole Automation MCP Server is running!"}
