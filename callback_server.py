from flask import Flask, request, jsonify
import json
from datetime import datetime
from order_manager import OrderManager, OrderStatus

app = Flask(__name__)
order_manager = OrderManager()

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
    
    # Update order status based on payment status
    if 'depositId' in data:
        deposit_id = data['depositId']
        status = data.get('status', '').upper()
        
        # print the orders in the order manager
        print(f"Orders in the order manager: {order_manager.orders}")
        # Find order by deposit_id and update its status
        for order in order_manager.orders.values():
            if order.deposit_id == deposit_id:
                if status == 'COMPLETED':
                    order_manager.update_order_status(
                        order.order_id,
                        OrderStatus.PAYMENT_SUCCESS,
                        payment_details=data
                    )
                elif status == 'REJECTED':
                    order_manager.update_order_status(
                        order.order_id,
                        OrderStatus.PAYMENT_FAILED,
                        payment_details=data
                    )
    
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

@app.route('/orders', methods=['GET'])
def view_orders():
    return jsonify({
        order_id: order.to_dict() 
        for order_id, order in order_manager.orders.items()
    })

@app.route('/orders/<order_id>', methods=['GET'])
def view_order(order_id):
    order = order_manager.get_order(order_id)
    if order:
        return jsonify(order.to_dict())
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 