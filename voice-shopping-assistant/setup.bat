@echo off
REM Voice Shopping Assistant - Quick Setup Script for Windows
REM This script sets up the entire development environment

echo.
echo 🛒 Voice Shopping Assistant - Setup Script
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH. Please install Node.js 16+
    exit /b 1
)

REM Create .env files
echo 📝 Creating environment files...

cd backend
(
    echo FLASK_ENV=development
    echo GOOGLE_CLOUD_CREDENTIALS=
    echo DATABASE=shopping_assistant.db
) > .env
cd ..

cd frontend
(
    echo VITE_API_URL=http://localhost:5000
) > .env
cd ..

echo ✓ Environment files created

REM Setup Backend
echo.
echo 🔧 Setting up backend...
cd backend

if not exist "venv" (
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt
python -m spacy download en_core_web_sm

echo ✓ Backend setup complete
cd ..

REM Setup Frontend
echo.
echo 🔧 Setting up frontend...
cd frontend

call npm install

echo ✓ Frontend setup complete
cd ..

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To start development:
echo.
echo   Terminal 1 (Backend^):
echo     cd backend
echo     venv\Scripts\activate.bat
echo     python run.py
echo.
echo   Terminal 2 (Frontend^):
echo     cd frontend
echo     npm run dev
echo.
echo   Then open http://localhost:3000 in your browser
echo.
echo 📚 Documentation:
echo   - README.md - Full documentation
echo   - APPROACH.md - Technical approach
echo   - DEPLOYMENT.md - Cloud deployment guide
echo.
pause
