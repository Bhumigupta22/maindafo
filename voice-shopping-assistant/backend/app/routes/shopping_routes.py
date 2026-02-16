from flask import Blueprint, request, jsonify
from app.database import (
    add_shopping_item, get_shopping_list, remove_shopping_item,
    mark_item_complete, add_to_history
)

bp = Blueprint('shopping', __name__, url_prefix='/api/shopping')

@bp.route('/list', methods=['GET'])
def get_list():
    """Get current shopping list"""
    try:
        items = get_shopping_list()
        return jsonify({'items': items, 'count': len(items)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/add', methods=['POST'])
def add_item():
    """Add item to shopping list"""
    try:
        data = request.get_json()
        item_name = data.get('item_name', '').strip()
        
        if not item_name:
            return jsonify({'error': 'Item name is required'}), 400
        
        category = data.get('category', 'other')
        quantity = data.get('quantity', 1)
        unit = data.get('unit', '')
        price = data.get('price')
        
        # Validate quantity
        try:
            quantity = float(quantity)
        except (ValueError, TypeError):
            quantity = 1
        
        item_id = add_shopping_item(item_name, category, quantity, unit, price)
        add_to_history(item_name, category)
        
        return jsonify({
            'success': True,
            'item_id': item_id,
            'item': {
                'id': item_id,
                'item_name': item_name,
                'category': category,
                'quantity': quantity,
                'unit': unit,
                'price': price
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:item_id>', methods=['DELETE'])
def remove_item(item_id):
    """Remove item from shopping list"""
    try:
        remove_shopping_item(item_id)
        return jsonify({'success': True, 'message': 'Item removed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:item_id>/complete', methods=['PUT'])
def complete_item(item_id):
    """Mark item as completed/purchased"""
    try:
        mark_item_complete(item_id)
        return jsonify({'success': True, 'message': 'Item marked as completed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
