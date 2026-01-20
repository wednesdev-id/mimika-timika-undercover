@echo off
SETLOCAL EnableDelayedExpansion

cd /d "%~dp0"

echo [Backend] Checking Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [Error] Python is not installed or not in PATH.
    echo Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

IF NOT EXIST ".venv" (
    echo [Backend] Creating virtual environment...
    python -m venv .venv
)

echo [Backend] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [Backend] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [Backend] Starting server...
echo [Backend] Scheduler will start automatically properly.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
