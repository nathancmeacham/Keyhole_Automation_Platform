@echo off
echo Starting Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
cd /d C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform

echo Activating virtual environment...
call .venv\Scripts\activate


echo Waiting a few seconds for Docker Desktop to start...
timeout /t 5

echo Running Qdrant container...
start "Qdrant Terminal" cmd /k "docker run -p 6333:6333 qdrant/qdrant"

start "FastAPI Terminal" cmd /k "cd /d C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform && call .venv\Scripts\activate && uvicorn backend.mcp.server:app --reload"

start "Frontend Terminal" cmd /k "cd /d C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform\frontend\Keyhole-Solution-App && npm start"

start "Production Terminal" cmd /k "cd /d C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform && call .venv\Scripts\activate"


