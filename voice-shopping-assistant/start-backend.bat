@echo off
echo.
echo ========================================
echo   Voice Shopping Assistant - Startup
echo ========================================
echo.
echo Starting backend... (Press Ctrl+C to stop)
echo Backend will run on: http://localhost:5000
echo.
cd /d "%~dp0backend"
python run.py
