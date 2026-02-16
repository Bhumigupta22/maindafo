from flask import Blueprint, jsonify
from app.database import get_purchase_history, get_shopping_list
from app.suggestions import get_suggestions

bp = Blueprint('suggestions', __name__, url_prefix='/api/suggestions')

@bp.route('/', methods=['GET'])
def get_smart_suggestions():
    """Get smart suggestions based on history and current list"""
    try:
        history = get_purchase_history()
        current_list = get_shopping_list()
        suggestions = get_suggestions(history, current_list)
        
        return jsonify({
            'suggestions': suggestions,
            'count': len(suggestions)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/history', methods=['GET'])
def get_history():
    """Get purchase history for user"""
    try:
        history = get_purchase_history()
        return jsonify({
            'history': history,
            'count': len(history)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
