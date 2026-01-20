@echo off
echo Starting Papua News - Local Dev Mode (No Docker)
echo =================================================

echo 1. Starting Backend Service (Port 8000)...
start "Backend Service" cmd /k "cd services/backend-service && pip install -r requirements.txt && python -m uvicorn app.main:app --reload --port 8000"

echo 2. Starting API Gateway...
echo NOTE: Since we are running locally without Nginx, the frontend will need to hit the Backend directly or via a simple Node proxy if running.
echo For simplicity in this mode, we will rely on the Backend running on port 8000.

echo 3. Starting Web Mimika (Port 8080)...
start "Web Mimika" cmd /k "cd apps/web-mimika && npm install && npm run dev"

echo 4. Starting Web Timika (Port 8081)...
start "Web Timika" cmd /k "cd apps/web-timika && npm install && npm run dev"

echo =================================================
echo All services started in separate windows.
echo - Backend: http://localhost:8000/docs
echo - Mimika: http://localhost:8080
echo - Timika: http://localhost:8081
echo =================================================
pause
