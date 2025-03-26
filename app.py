from flask import Flask, request, jsonify

app = Flask(__name__)

# Тимчасове зберігання даних
menu = [
    {"id": 1, "name": "Кава", "price": 50},
    {"id": 2, "name": "Чай", "price": 30}
]
orders = []
clients = []

# --- Меню ---
@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(menu)

@app.route('/menu', methods=['POST'])
def add_item():
    new_item = request.json
    menu.append(new_item)
    return jsonify(new_item), 201

@app.route('/menu/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            item.update(request.json)
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global menu
    menu = [item for item in menu if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

# --- Замовлення ---
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    new_order = request.json
    orders.append(new_order)
    return jsonify(new_order), 201

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    for order in orders:
        if order["id"] == order_id:
            order.update(request.json)
            return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    global orders
    orders = [order for order in orders if order["id"] != order_id]
    return jsonify({"message": "Order deleted"}), 200

# --- Клієнти ---
@app.route('/clients', methods=['GET'])
def get_clients():
    return jsonify(clients)

@app.route('/clients', methods=['POST'])
def add_client():
    new_client = request.json
    clients.append(new_client)
    return jsonify(new_client), 201

@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    for client in clients:
        if client["id"] == client_id:
            client.update(request.json)
            return jsonify(client)
    return jsonify({"error": "Client not found"}), 404

@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    global clients
    clients = [client for client in clients if client["id"] != client_id]
    return jsonify({"message": "Client deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
