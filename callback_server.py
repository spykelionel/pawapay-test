from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Store callbacks in memory (in production, you'd want to use a database)
callbacks = {
    'deposits': [],
    'payouts': [],
    'refunds': []
}

@app.route('/deposits', methods=['POST'])
def deposit_callback():
    data = request.json
    callback_data = {
        'timestamp': datetime.now().isoformat(),
        'type': 'deposit',
        'data': data
    }
    callbacks['deposits'].append(callback_data)
    print(f"Received deposit callback: {json.dumps(data, indent=2)}")
    return jsonify({"status": "success"}), 200

@app.route('/payouts', methods=['POST'])
def payout_callback():
    data = request.json
    callback_data = {
        'timestamp': datetime.now().isoformat(),
        'type': 'payout',
        'data': data
    }
    callbacks['payouts'].append(callback_data)
    print(f"Received payout callback: {json.dumps(data, indent=2)}")
    return jsonify({"status": "success"}), 200

@app.route('/refunds', methods=['POST'])
def refund_callback():
    data = request.json
    callback_data = {
        'timestamp': datetime.now().isoformat(),
        'type': 'refund',
        'data': data
    }
    callbacks['refunds'].append(callback_data)
    print(f"Received refund callback: {json.dumps(data, indent=2)}")
    return jsonify({"status": "success"}), 200

@app.route('/view', methods=['GET'])
def view_callbacks():
    return jsonify(callbacks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 