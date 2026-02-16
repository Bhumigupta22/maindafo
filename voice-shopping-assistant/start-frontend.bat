@echo off
echo.
echo ========================================
echo   Voice Shopping Assistant - Frontend
echo ========================================
echo.
echo Starting frontend... (Press Ctrl+C to stop)
echo Frontend will run on: http://localhost:3000
echo.
cd /d "%~dp0frontend"
npm run dev
