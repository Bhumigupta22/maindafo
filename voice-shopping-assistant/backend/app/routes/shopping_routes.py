from flask import Blueprint, request, jsonify
from app.database import (
    add_shopping_item, get_shopping_list, remove_shopping_item,
    mark_item_complete, add_to_history, get_db, remove_item_by_name
)

bp = Blueprint('shopping', __name__, url_prefix='/api/shopping')

@bp.route('/list', methods=['GET'])
def get_list():
    try:
        items = get_shopping_list()
        # Transform for Frontend: 'item_name' -> 'name'
        formatted = [{'id': i['id'], 'name': i['item_name'], 'category': i['category'], 'quantity': i['quantity']} for i in items]
        return jsonify(formatted), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/add', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        name = data.get('name') or data.get('item_name')
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        item_id = add_shopping_item(name, data.get('category', 'other'), data.get('quantity', 1))
        return jsonify({'id': item_id, 'name': name, 'category': data.get('category', 'other')}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/delete/<int:item_id>', methods=['DELETE', 'POST'])
def delete_item(item_id):
    try:
        success = remove_shopping_item(item_id)
        return jsonify({'success': success}), 200 if success else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500