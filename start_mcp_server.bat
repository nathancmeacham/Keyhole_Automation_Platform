@echo off
setlocal
set PORT=8000
set VENV_PATH=.venv\Scripts
set MODULE=backend.mcp.server:app

echo 🧠 Killing all lingering processes...

REM Kill anything on port 8000
FOR /F "tokens=5" %%P IN ('netstat -aon ^| findstr :%PORT% ^| findstr LISTENING') DO (
    echo 🔪 Killing port-bound PID %%P ...
    taskkill /F /PID %%P >nul 2>&1
)

REM Kill ALL rogue Python subprocesses (uvicorn reload or dev tools)
echo 🔪 Killing all python.exe processes (if running server)...
taskkill /F /IM python.exe /T >nul 2>&1

REM Give OS time to release the port
echo ⏳ Waiting for port %PORT% to be released...
timeout /t 3 >nul

REM Verify port is free
FOR /F "tokens=5" %%P IN ('netstat -aon ^| findstr :%PORT% ^| findstr LISTENING') DO (
    echo ❌ Port %PORT% is still in use (PID: %%P). Aborting.
    goto END
)

REM Start server
echo 🚀 Starting MCP server...
cd /d "%~dp0"
%VENV_PATH%\uvicorn.exe %MODULE% --host 127.0.0.1 --port %PORT% --log-level debug

:END
echo.
