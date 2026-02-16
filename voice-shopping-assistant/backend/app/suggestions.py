from typing import List, Dict
from datetime import datetime, timedelta
import math

class SuggestionEngine:
    """Generate smart suggestions based on history and seasonal items"""
    
    SEASONAL_ITEMS = {
        'spring': {
            'produce': ['strawberry', 'asparagus', 'spinach', 'pea', 'lettuce'],
            'seasonal': True
        },
        'summer': {
            'produce': ['watermelon', 'peach', 'blueberry', 'corn', 'tomato'],
            'seasonal': True
        },
        'fall': {
            'produce': ['apple', 'pumpkin', 'squash', 'cranberry', 'pear'],
            'seasonal': True
        },
        'winter': {
            'produce': ['orange', 'lemon', 'grapefruit', 'kale', 'kiwi'],
            'seasonal': True
        }
    }
    
    SUBSTITUTES = {
        'milk': ['almond milk', 'oat milk', 'coconut milk', 'soy milk'],
        'bread': ['whole wheat bread', 'rye bread', 'gluten-free bread'],
        'apple': ['pear', 'orange', 'banana'],
        'chicken': ['turkey', 'tofu', 'seitan'],
        'sugar': ['honey', 'maple syrup', 'stevia']
    }
    
    def __init__(self):
        self.current_season = self._get_current_season()
    
    def _get_current_season(self) -> str:
        """Determine current season based on month"""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'fall'
        else:
            return 'winter'
    
    def get_frequent_items(self, history: List[Dict], limit: int = 5) -> List[Dict]:
        """Get items the user frequently buys"""
        if not history:
            return []
        
        # Sort by frequency and return top items
        sorted_history = sorted(history, key=lambda x: x.get('frequency', 0), reverse=True)
        return sorted_history[:limit]
    
    def get_seasonal_recommendations(self, limit: int = 3) -> List[Dict]:
        """Get seasonal item recommendations"""
        seasonal_items = self.SEASONAL_ITEMS.get(self.current_season, {})
        recommendations = []
        
        for category, items in seasonal_items.items():
            for i, item in enumerate(items[:limit]):
                recommendations.append({
                    'item': item,
                    'category': category.replace('_', ''),
                    'reason': f'In season ({self.current_season})',
                    'confidence': 0.9 - (i * 0.1)
                })
        
        return recommendations[:limit]
    
    def get_substitutes(self, item_name: str) -> List[Dict]:
        """Get alternative products for an item"""
        item_lower = item_name.lower()
        
        for key, substitutes in self.SUBSTITUTES.items():
            if key in item_lower:
                return [
                    {
                        'item': sub,
                        'reason': f'Alternative to {item_name}',
                        'confidence': 0.85
                    }
                    for sub in substitutes
                ]
        
        return []
    
    def get_smart_suggestions(self, 
                            purchase_history: List[Dict],
                            current_list: List[Dict]) -> List[Dict]:
        """Generate comprehensive smart suggestions"""
        suggestions = []
        current_items = {item['item_name'].lower() for item in current_list}
        
        # Add frequently purchased items that aren't in current list
        frequent_items = self.get_frequent_items(purchase_history, 5)
        
        for item in frequent_items:
            if item['item_name'].lower() not in current_items:
                suggestions.append({
                    'item': item['item_name'],
                    'category': item.get('category', 'other'),
                    'reason': f"You usually buy {item['item_name']} (bought {item.get('frequency', 0)} times)",
                    'suggestion_type': 'history_based',
                    'confidence': min(0.95, 0.6 + (item.get('frequency', 0) * 0.05))
                })
        
        # Add seasonal recommendations
        seasonal = self.get_seasonal_recommendations(3)
        current_items_lower = {s['item'].lower() for s in suggestions}
        for item in seasonal:
            if item['item'].lower() not in current_items_lower and item['item'].lower() not in current_items:
                item['suggestion_type'] = 'seasonal'
                suggestions.append(item)
        
        # If no suggestions from history or seasonal, add common items
        if len(suggestions) == 0:
            common_items = [
                {'item': 'milk', 'category': 'dairy', 'reason': 'Popular staple', 'suggestion_type': 'default', 'confidence': 0.85},
                {'item': 'bread', 'category': 'pantry', 'reason': 'Essential grocery', 'suggestion_type': 'default', 'confidence': 0.85},
                {'item': 'eggs', 'category': 'dairy', 'reason': 'Frequently purchased', 'suggestion_type': 'default', 'confidence': 0.85},
                {'item': 'butter', 'category': 'dairy', 'reason': 'Common staple', 'suggestion_type': 'default', 'confidence': 0.80},
                {'item': 'chicken', 'category': 'meat', 'reason': 'Popular protein', 'suggestion_type': 'default', 'confidence': 0.80},
            ]
            for item in common_items:
                if item['item'].lower() not in current_items:
                    suggestions.append(item)
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        return suggestions[:5]  # Return top 5

# Global instance
suggestion_engine = SuggestionEngine()

def get_suggestions(purchase_history: List[Dict], current_list: List[Dict]) -> List[Dict]:
    """Convenience function to get smart suggestions"""
    return suggestion_engine.get_smart_suggestions(purchase_history, current_list)
