# Keyhole_Automation_Platform\backend\mcp\src\config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    MCP_PORT: int = 8000
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        extra = "allow"  # ✅ This allows extra environment variables without errors

settings = Settings()
