#!/usr/bin/env python3
"""
Integration test script to verify the Voice Shopping Assistant setup
Run this after installation to ensure everything is working correctly
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all required modules can be imported"""
    print("📦 Testing imports...")
    try:
        from app.nlp_processor import NLPProcessor
        from app.database import init_db, add_shopping_item, get_shopping_list
        from app.voice_processor import VoiceProcessor
        from app.suggestions import SuggestionEngine
        print("  ✓ All imports successful")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

def test_database():
    """Test database operations"""
    print("📊 Testing database...")
    try:
        from app.database import init_db, add_shopping_item, get_shopping_list, remove_shopping_item
        
        # Initialize database
        init_db()
        print("  ✓ Database initialized")
        
        # Test add item
        item_id = add_shopping_item("Test Milk", "dairy", 1, "bottle")
        print(f"  ✓ Item added (ID: {item_id})")
        
        # Test get items
        items = get_shopping_list()
        if items:
            print(f"  ✓ Retrieved {len(items)} item(s)")
        else:
            print("  ✗ No items retrieved")
            return False
        
        # Test remove item
        remove_shopping_item(item_id)
        print("  ✓ Item removed")
        
        return True
    except Exception as e:
        print(f"  ✗ Database test failed: {e}")
        return False

def test_nlp():
    """Test NLP processor"""
    print("🧠 Testing NLP processor...")
    try:
        from app.nlp_processor import NLPProcessor
        
        nlp = NLPProcessor()
        
        # Test 1: Simple add command
        result = nlp.process_voice_command("Add milk")
        assert result["command"] == "add", "Failed to parse add command"
        assert "milk" in result["item_name"].lower(), "Failed to extract item name"
        print("  ✓ Simple command parsing works")
        
        # Test 2: Quantity extraction
        result = nlp.process_voice_command("Add 2 bottles of water")
        assert result["quantity"] == 2.0, "Failed to extract quantity"
        print("  ✓ Quantity extraction works")
        
        # Test 3: Category detection
        result = nlp.process_voice_command("Add cheese")
        assert result["category"] == "dairy", "Failed to categorize item"
        print("  ✓ Category detection works")
        
        # Test 4: Remove command
        result = nlp.process_voice_command("Remove milk from my list")
        assert result["command"] == "remove", "Failed to parse remove command"
        print("  ✓ Remove command parsing works")
        
        return True
    except Exception as e:
        print(f"  ✗ NLP test failed: {e}")
        return False

def test_suggestions():
    """Test suggestion engine"""
    print("🎯 Testing suggestions engine...")
    try:
        from app.suggestions import SuggestionEngine
        
        engine = SuggestionEngine()
        
        # Test 1: Get seasonal recommendations
        seasonal = engine.get_seasonal_recommendations(3)
        assert len(seasonal) <= 3, "Too many seasonal recommendations"
        print(f"  ✓ Seasonal recommendations work ({len(seasonal)} items)")
        
        # Test 2: Get substitutes
        subs = engine.get_substitutes("milk")
        assert len(subs) > 0, "No substitutes found for milk"
        print(f"  ✓ Substitute recommendations work ({len(subs)} alternatives)")
        
        # Test 3: Get smart suggestions
        history = [
            {"item_name": "milk", "category": "dairy", "frequency": 5},
            {"item_name": "bread", "category": "pantry", "frequency": 3}
        ]
        current = [{"item_name": "cheese", "category": "dairy"}]
        suggestions = engine.get_smart_suggestions(history, current)
        print(f"  ✓ Smart suggestions work ({len(suggestions)} suggestions)")
        
        return True
    except Exception as e:
        print(f"  ✗ Suggestions test failed: {e}")
        return False

def test_voice_processor():
    """Test voice processor"""
    print("🎤 Testing voice processor...")
    try:
        from app.voice_processor import VoiceProcessor
        
        processor = VoiceProcessor()
        
        # Test availability
        available = processor.is_available()
        if available:
            print("  ✓ Google Cloud Speech API configured")
        else:
            print("  ⚠ Using mock voice recognition (Google Cloud not configured)")
            print("    To enable: Set GOOGLE_CLOUD_CREDENTIALS in .env")
        
        return True
    except Exception as e:
        print(f"  ✗ Voice processor test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Voice Shopping Assistant - Setup Verification")
    print("=" * 50)
    print()
    
    tests = [
        test_imports,
        test_database,
        test_nlp,
        test_suggestions,
        test_voice_processor
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    # Summary
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed! ({passed}/{total})")
        print()
        print("🚀 Ready to start development:")
        print()
        print("  Backend:  python backend/run.py")
        print("  Frontend: cd frontend && npm run dev")
        print()
        return 0
    else:
        print(f"❌ Some tests failed: {passed}/{total} passed")
        print()
        print("📖 See errors above and check:")
        print("  - Python dependencies installed: pip install -r backend/requirements.txt")
        print("  - spaCy model: python -m spacy download en_core_web_sm")
        print("  - Node.js installed: node --version")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
