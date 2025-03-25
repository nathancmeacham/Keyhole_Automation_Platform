@echo off
echo Starting Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
cd /d C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform
taskkill /F /IM python.exe /T
echo Activating virtual environment...
call .venv\Scripts\activate


echo Waiting a few seconds for Docker Desktop to start...
timeout /t 8


echo 🔍 Checking for running Qdrant container...
REM Find container running qdrant
FOR /F "tokens=*" %%i IN ('docker ps -q --filter "ancestor=qdrant/qdrant"') DO (
    echo 🛑 Stopping container %%i
    docker stop %%i
    echo ❌ Removing container %%i
    docker rm %%i
)
echo 🔍 Checking for running Qdrant container...
start "Qdrant Terminal" cmd /k "docker compose up -d qdrant"

start "FastAPI Terminal" cmd /k "cd /d C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform && call .venv\Scripts\activate && uvicorn backend.mcp.server:app"

start "Frontend Terminal" cmd /k "cd /d C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform\frontend\Keyhole-Solution-App && npm start"

start "Production Terminal" cmd /k "cd /d C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform && call .venv\Scripts\activate"

