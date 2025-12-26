import uuid

from flask import Flask, jsonify, request

order_app = Flask(__name__)

# Keeping all the orders in memory
ORDERS = {}


def generate_uuid():
    return str(uuid.uuid4())

@order_app.route('/orders', methods=['POST'])
def create_order():
    uuid = generate_uuid()
    ORDERS[uuid] = request.get_json()
    return jsonify({"order_id": uuid})

@order_app.route('/orders/<order_id>', methods=['GET'])
def create_order(order_id):
    if order_id in ORDERS:
        return jsonify(ORDERS[order_id])
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    order_app.run(port=5002)