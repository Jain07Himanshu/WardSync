@echo off
title WardSync Platform Launcher
echo ===============================================================================
echo                WARDSYNC: CIVIC DISCOVERY ^& ACTION PLATFORM
echo         Connecting civic_engine + civic_pipeline + wardsync-frontend
echo ===============================================================================
echo.
echo Starting Unified Backend on http://127.0.0.1:8000 ...
start "WardSync Unified Backend" cmd /k "python run.py"

timeout /t 2 /nobreak >nul

echo Starting WardSync Frontend on http://localhost:5173 ...
cd wardsync-frontend
start "WardSync Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ===============================================================================
echo All services launched!
echo - Backend API & Swagger Docs: http://127.0.0.1:8000/docs
echo - Frontend User Interface:    http://localhost:5173
echo ===============================================================================
