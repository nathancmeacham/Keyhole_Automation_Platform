# Keyhole_Automation_Platform\tests\backend\mcp\test_config.py
from backend.mcp.src.config import settings  # ✅ Ensure correct path

def test_config_values():
    """Test if configuration values load correctly from .env"""
    assert settings.ENV == "development"
    assert settings.DEBUG is True
    assert settings.MCP_PORT == 8000
    assert settings.LOG_LEVEL == "info"
