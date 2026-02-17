import re
from typing import Dict, Tuple

class NLPProcessor:
    CATEGORIES = {
        'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream'],
        'produce': ['apple', 'banana', 'orange', 'carrot', 'broccoli', 'lettuce', 'tomato'],
        'meat': ['chicken', 'beef', 'pork', 'fish', 'sausage'],
        'snacks': ['chips', 'cookies', 'popcorn', 'nuts', 'candy'],
        'beverages': ['water', 'juice', 'soda', 'coffee', 'tea'],
        'pantry': ['bread', 'rice', 'pasta', 'cereal', 'rolls']
    }
    
    COMMANDS = {
        'remove': ['remove', 'delete', 'discard', 'skip', 'cancel', 'don\'t need'],
        'add': ['add', 'buy', 'get', 'need', 'want', 'put', 'grab']
    }

    def process_voice_command(self, text: str) -> Dict:
        if not text or not text.strip():
            return {'error': 'Empty command'}
        
        text_lower = text.lower().strip()
        command_type = 'add'
        
        if any(word in text_lower for word in self.COMMANDS['remove']):
            command_type = 'remove'

        item_name = text_lower
        # List of words to strip out of the item name
        strip_words = self.COMMANDS['add'] + self.COMMANDS['remove'] + ['please', 'to my list', 'from my list', 'the', 'a', 'an']
        
        for word in strip_words:
            item_name = re.sub(rf'\b{re.escape(word)}\b', '', item_name)
        
        # Extract and strip numbers
        number_match = re.search(r'(\d+)', item_name)
        quantity = 1
        if number_match:
            quantity = float(number_match.group(1))
            item_name = item_name.replace(str(int(quantity)), '')

        item_name = ' '.join(item_name.split()).strip()

        return {
            'command': command_type,
            'item_name': item_name,
            'quantity': quantity,
            'category': self.extract_category(item_name),
            'original_text': text
        }

    def extract_category(self, item: str) -> str:
        for category, items in self.CATEGORIES.items():
            if any(cat_item in item.lower() for cat_item in items):
                return category
        return 'other'

nlp_processor = NLPProcessor()
def process_command(text: str) -> Dict:
    return nlp_processor.process_voice_command(text)