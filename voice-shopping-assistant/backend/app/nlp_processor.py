import re
from typing import Dict, Tuple

class NLPProcessor:
    """Process natural language for shopping commands"""
    
    CATEGORIES = {
        'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream'],
        'produce': ['apple', 'banana', 'orange', 'carrot', 'broccoli', 'lettuce', 'tomato'],
        'meat': ['chicken', 'beef', 'pork', 'fish', 'salmon'],
        'snacks': ['chips', 'cookies', 'popcorn', 'nuts', 'candy'],
        'beverages': ['water', 'juice', 'soda', 'coffee', 'tea'],
        'pantry': ['bread', 'rice', 'pasta', 'cereal', 'flour', 'sugar']
    }
    
    COMMANDS = {
        'add': ['add', 'buy', 'get', 'i need', 'i want', 'pick up',
                'purchase', 'include', 'grab', 'put'],
        'remove': ['remove', 'delete', 'discard', 'skip', 'don\'t need', 'cancel'],
        'quantity': ['amount', 'quantity', 'number', 'bottles', 'boxes', 'bags']
    }
    
    def __init__(self):
        self.nlp = None  # spaCy is optional, app works without it
    
    def extract_command(self, text: str) -> str:
        """Identify the command type (add, remove, search)"""
        text_lower = text.lower()
        
        for cmd, keywords in self.COMMANDS.items():
            if any(keyword in text_lower for keyword in keywords):
                return cmd if cmd != 'quantity' else 'quantity'
        
        return 'add'  # Default to add
    
    def extract_category(self, item: str) -> str:
        """Categorize the item"""
        item_lower = item.lower()
        
        for category, items in self.CATEGORIES.items():
            if any(cat_item in item_lower for cat_item in items):
                return category
        
        return 'other'
    
    def extract_quantity(self, text: str) -> Tuple[float, str]:
        """Extract quantity and unit from text"""
        text_lower = text.lower()
        
        # Look for number patterns
        import re
        number_pattern = r'(\d+(?:\.\d+)?)\s*(bottle|box|bag|kg|g|lb|ounce|piece|pieces)?'
        match = re.search(number_pattern, text_lower)
        
        if match:
            quantity = float(match.group(1))
            unit = match.group(2) or ''
            return quantity, unit
        
        return 1, ''
    
    def process_voice_command(self, text: str) -> Dict:
        """Process a voice command and extract structured data"""
        if not text or not text.strip():
            return {'error': 'Empty command'}
        
        command_type = self.extract_command(text)
        
        # Extract item name (remove command keywords)
        item_name = text
        for keywords in self.COMMANDS.values():
            for keyword in keywords:
                item_name = re.sub(rf'\b{re.escape(keyword)}\b', '', item_name, flags=re.IGNORECASE)
        
        # Remove trailing phrases like "to my list", "to the list", "please"
        item_name = re.sub(r'\s+(to\s+)?(my|the|a)\s+(list|shopping|cart).*$', '', item_name, flags=re.IGNORECASE)
        item_name = re.sub(r'\s+please\s*$', '', item_name, flags=re.IGNORECASE)
        
        # Remove extra spaces
        item_name = ' '.join(item_name.split()).strip()
        
        if not item_name:
            return {'error': 'Could not extract item name'}
        
        quantity, unit = self.extract_quantity(text)
        category = self.extract_category(item_name)
        
        return {
            'command': command_type,
            'item_name': item_name,
            'quantity': quantity,
            'unit': unit,
            'category': category,
            'original_text': text
        }

# Global instance
nlp_processor = NLPProcessor()

def process_command(text: str) -> Dict:
    """Convenience function to process a command"""
    return nlp_processor.process_voice_command(text)
