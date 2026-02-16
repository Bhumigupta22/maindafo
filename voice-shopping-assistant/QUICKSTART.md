# Quick Start Guide

Get the Voice Shopping Assistant running in **5 minutes**.

## Prerequisites

- **Windows:** Python 3.8+, Node.js 16+
- **Mac/Linux:** Python 3.8+, Node.js 16+

## Installation (Windows)

```bash
# 1. Extract or navigate to project folder
cd voice-shopping-assistant

# 2. Run setup script
setup.bat

# 3. In one terminal, start backend:
cd backend
venv\Scripts\activate.bat
python run.py

# 4. In another terminal, start frontend:
cd frontend
npm run dev

# 5. Open browser to http://localhost:3000
```

## Installation (Mac/Linux)

```bash
# 1. Navigate to project folder
cd voice-shopping-assistant

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. In one terminal, start backend:
cd backend
source venv/bin/activate
python run.py

# 4. In another terminal, start frontend:
cd frontend
npm run dev

# 5. Open browser to http://localhost:3000
```

## Installation (Docker)

```bash
# 1. Make sure Docker is installed and running

# 2. Run Docker Compose
docker-compose up

# 3. Frontend available at http://localhost:3000
# 4. Backend API at http://localhost:5000
```

## Verify Installation

```bash
python verify_setup.py
```

This will test:
- ✓ All modules import correctly
- ✓ Database operations work
- ✓ NLP processor functions
- ✓ Suggestions engine works
- ✓ Voice processor is available

## Using the App

1. **Click the microphone button** 🎤
2. **Speak a command**:
   - "Add milk to my list"
   - "I need 2 bottles of water"
   - "Remove apples"
   - "Buy cheese"
3. **See items appear** in your shopping list
4. **Get smart suggestions** based on your history

## Example Commands

| Command | What Happens |
|---------|--------------|
| "Add milk" | Adds milk to dairy category |
| "Buy 3 oranges" | Adds 3 oranges to produce |
| "I need bread" | Adds bread to pantry category |
| "Remove milk" | Removes milk from list |
| "Show suggestions" | Shows recommended items |

## Troubleshooting

### Port Already in Use
```bash
# Backend on 5000
lsof -i :5000

# Frontend on 3000
lsof -i :3000
```

### Permission Denied (Linux/Mac)
```bash
chmod +x setup.sh
chmod +x verify_setup.py
```

### Module Not Found
```bash
# Backend
cd backend && pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Frontend
cd frontend && npm install
```

## Next Steps

- 📖 Read [README.md](README.md) for full documentation
- 🏗️ Check [APPROACH.md](APPROACH.md) for architecture
- 🚀 Deploy to cloud with [DEPLOYMENT.md](DEPLOYMENT.md)
- 🔨 Extend features with [DEV_GUIDE.md](DEV_GUIDE.md)

## Support

- GitHub Issues: [Report bugs](https://github.com/your-username/voice-shopping-assistant/issues)
- Discussions: [Ask questions](https://github.com/your-username/voice-shopping-assistant/discussions)

---

**Happy shopping! 🛒**
