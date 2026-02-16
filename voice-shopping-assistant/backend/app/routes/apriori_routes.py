from flask import Blueprint, request, jsonify
from app.apriori import engine, load_transactions_from_json
from app.database import get_purchase_history

bp = Blueprint('apriori', __name__, url_prefix='/api/suggestions/apriori')


@bp.route('/', methods=['GET'])
def query_apriori():
    """Get apriori-based recommendations for an item"""
    try:
        item = request.args.get('item')
        if not item:
            return jsonify({'error': 'item query parameter is required'}), 400

        min_conf = float(request.args.get('min_confidence', 0.2))
        top_n = int(request.args.get('top_n', 5))

        recs = engine.get_recommendations(item, top_n=top_n, min_confidence=min_conf)
        return jsonify({'recommendations': recs}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/upload', methods=['POST'])
def upload_transactions():
    """Upload transactions (JSON array or CSV file) to build Apriori model"""
    try:
        # prefer file upload
        if 'file' in request.files:
            f = request.files['file']
            content = f.read().decode('utf-8')
            # try parse as json
            try:
                data = json.loads(content)
            except Exception:
                # fallback: csv with one transaction per line
                lines = [l.strip() for l in content.splitlines() if l.strip()]
                data = [l.split(',') for l in lines]

            transactions = load_transactions_from_json(data)
        else:
            payload = request.get_json() or {}
            data = payload.get('transactions')
            transactions = load_transactions_from_json(data) if data else []

        if not transactions:
            # fallback: try to build synthetic transactions from purchase_history
            history = get_purchase_history()
            # history is list of {item_name, category, frequency}
            transactions = []
            for h in history:
                # create 'frequency' transactions that include the item
                freq = max(1, int(h.get('frequency', 1)))
                for _ in range(freq):
                    transactions.append([h['item_name'].lower()])

        rules = engine.fit(transactions, min_support=0.02, min_confidence=0.25)
        return jsonify({'rules_count': len(rules)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
