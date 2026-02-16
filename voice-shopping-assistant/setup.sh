#!/bin/bash

# Voice Shopping Assistant - Quick Setup Script
# This script sets up the entire development environment

set -e

echo "🛒 Voice Shopping Assistant - Setup Script"
echo "=========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

# Create .env files
echo "📝 Creating environment files..."

# Backend .env
cat > backend/.env << EOF
FLASK_ENV=development
GOOGLE_CLOUD_CREDENTIALS=
DATABASE=shopping_assistant.db
EOF

# Frontend .env
cat > frontend/.env << EOF
VITE_API_URL=http://localhost:5000
EOF

echo "✓ Environment files created"

# Setup Backend
echo "🔧 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

echo "✓ Backend setup complete"
cd ..

# Setup Frontend
echo "🔧 Setting up frontend..."
cd frontend

# Install dependencies
npm install

echo "✓ Frontend setup complete"
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start development:"
echo ""
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    python run.py"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd frontend"
echo "    npm run dev"
echo ""
echo "  Then open http://localhost:3000 in your browser"
echo ""
echo "📚 Documentation:"
echo "  - README.md - Full documentation"
echo "  - APPROACH.md - Technical approach"
echo "  - DEPLOYMENT.md - Cloud deployment guide"
