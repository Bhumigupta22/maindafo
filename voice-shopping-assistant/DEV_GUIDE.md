# Development Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Port 3000)               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Voice Input  │  Shopping List  │  Suggestions       │  │
│  │  Component   │    Component    │   Component        │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST API
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Flask Backend API (Port 5000)                  │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │  Shopping  │  │    Voice    │  │  Suggestions     │  │
│  │  Routes    │  │    Routes   │  │   Routes         │  │
│  └────────────┘  └─────────────┘  └──────────────────┘  │
│         ↓              ↓                  ↓                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  NLP Processor │  Voice Processor │  Suggestions      │  │
│  │  (spaCy)       │  (Google Cloud)  │  Engine           │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ SQL
                           ↓
                    ┌──────────────┐
                    │  SQLite DB   │
                    │  (or Cloud SQL)
                    └──────────────┘
```

## File Structure Reference

### Backend Files

**Core Application**
- `run.py` - Application entry point
- `app/__init__.py` - Flask app factory
- `app/config.py` - Configuration management

**Features**
- `app/nlp_processor.py` - Natural language processing
- `app/voice_processor.py` - Voice recognition
- `app/suggestions.py` - Recommendation engine
- `app/database.py` - Database operations

**API Routes**
- `app/routes/shopping_routes.py` - Shopping list endpoints
- `app/routes/voice_routes.py` - Voice processing endpoints
- `app/routes/suggestion_routes.py` - Suggestions endpoints

### Frontend Files

**Core**
- `main.jsx` - React entry point
- `App.jsx` - Main app component
- `api.js` - API client

**Components**
- `components/VoiceInput.jsx` - Voice recording & transcription
- `components/ShoppingList.jsx` - Shopping list display
- `components/Suggestions.jsx` - Smart suggestions panel

## Running Tests

### Backend Unit Tests

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run specific test file
python tests/test_nlp.py
python tests/test_database.py

# Or use pytest
pip install pytest
pytest tests/ -v
```

### Frontend Manual Testing

```bash
cd frontend
npm run dev

# Open http://localhost:3000
# Test voice input: Click microphone button and speak
# Test commands: "Add milk", "Remove apples", etc.
```

## Debugging

### Backend Debugging

```python
# Add debug prints
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Processing command: {text}")
```

### Frontend Debugging

```javascript
// Use browser DevTools (F12)
// Chrome/Firefox:
// 1. Open DevTools
// 2. Go to Console tab
// 3. Check Network tab for API calls

console.log('Debugging info:', variable);
```

## Common Issues & Solutions

### Issue: "Module not found: spacy"
**Solution:**
```bash
cd backend && source venv/bin/activate
python -m spacy download en_core_web_sm
```

### Issue: "Microphone permission denied"
**Solution:**
- Chrome: Allow microphone permission when prompted
- Firefox: Check privacy settings

### Issue: Backend API returns 404
**Solution:**
```bash
# Check backend is running
curl http://localhost:5000/api/shopping/list

# Check VITE_API_URL in frontend .env
# Should point to http://localhost:5000
```

### Issue: "Cannot connect to Google Cloud Speech API"
**Solution:**
- Download service account JSON key from Google Cloud Console
- Update `.env` file with correct `GOOGLE_CLOUD_CREDENTIALS` path
- Or the app will fallback to mock transcription

## Performance Optimization

### Frontend Optimization
1. **Lazy Load Suggestions** - Only fetch when component mounts
2. **Memoize Components** - Prevent unnecessary re-renders
3. **Bundle Size** - Check with `npm run build`

### Backend Optimization
1. **Database Indexing** - Add indexes to frequently queried fields
2. **Caching** - Cache suggestions for better performance
3. **Connection Pooling** - Use SQLAlchemy connection pools

## Security Best Practices

1. **Never commit secrets** - Use .env files
2. **Validate all inputs** - Sanitize user data
3. **Use HTTPS** - Enable in production
4. **CORS Configuration** - Whitelist specific origins
5. **Rate Limiting** - Implement on API endpoints

## Extending the Application

### Adding a New Voice Command

1. Update `nlp_processor.py`:
```python
COMMANDS = {
    'search': ['search', 'find', 'look for'],  # Add new command
    # ... other commands
}
```

2. Handle the command in routes:
```python
if result.data.command === 'search':
    # Implement search logic
```

### Adding a New Suggestion Type

1. Update `suggestions.py`:
```python
def get_custom_recommendations(self) -> List[Dict]:
    # Your recommendation logic
    return []

def get_smart_suggestions(self, ...):
    # Include custom recommendations
    custom = self.get_custom_recommendations()
```

### Adding a New Category

1. Update `nlp_processor.py`:
```python
CATEGORIES = {
    'dairy': [...],
    'new_category': ['item1', 'item2'],  # Add new category
}
```

## Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Frontend built (`npm run build`)
- [ ] Backend dependencies frozen (`pip freeze > requirements.txt`)
- [ ] Docker images build successfully
- [ ] Google Cloud credentials set up
- [ ] README updated with instructions
- [ ] CHANGELOG updated with version info

---

**Happy Coding!** 🚀
