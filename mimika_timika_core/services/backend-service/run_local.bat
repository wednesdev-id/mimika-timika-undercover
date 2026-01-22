@echo off
SETLOCAL EnableDelayedExpansion

cd /d "%~dp0"

echo [Backend] Checking Python...
IF NOT EXIST ".venv\Scripts\python.exe" (
    echo [Backend] Virtual environment not found or broken. Recreating...
    rmdir /s /q .venv 2>nul
    python -m venv .venv
)

echo [Backend] Using Virtual Environment at %CD%\.venv
echo.
echo [Backend] Installing dependencies directly into venv...

:: Use direct path to pip in venv to ensure we install to the correct place
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
".venv\Scripts\python.exe" -m pip install apscheduler

echo.
echo [Backend] Starting server using venv Python...
echo [Backend] Scheduler initialized.
echo.
".venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
