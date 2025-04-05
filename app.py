from flask import Flask, request, jsonify

app = Flask(__name__)

# Тимчасове зберігання даних
menu = [
    {"id": 1, "name": "Кава", "price": 50},
    {"id": 2, "name": "Чай", "price": 30}
]
clients = [
    {
        "id": 1,
        "name": "Анна",
        "phone": "+380501234567"
    },
    {
        "id": 2,
        "name": "Олександр",
        "phone": "+380971234567"
    }
]
orders = []
order_counter = 1  # Лічильник ID для замовлень


# --- Меню ---
@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(menu)


@app.route('/menu', methods=['POST'])
def add_item():
    new_item = request.json
    menu.append(new_item)
    return jsonify(new_item), 201


# --- Клієнти ---
@app.route('/clients', methods=['GET'])
def get_clients():
    return jsonify(clients)


@app.route('/clients', methods=['POST'])
def add_client():
    new_client = request.json
    clients.append(new_client)
    return jsonify(new_client), 201


# --- Замовлення ---
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)


@app.route('/orders', methods=['POST'])
def create_order():
    global order_counter
    data = request.json
    client_id = data.get("client_id")
    items = data.get("items", [])  # Очікується список об'єктів {"id": item_id, "quantity": кількість}

    # Перевіряємо, чи існує клієнт
    if not any(client["id"] == client_id for client in clients):
        return jsonify({"error": "Client not found"}), 404

    # Створюємо список обраних товарів із кількістю
    selected_items = []
    total_price = 0

    for item in items:
        menu_item = next((m for m in menu if m["id"] == item["id"]), None)
        if menu_item:
            quantity = item.get("quantity", 1)
            selected_items.append({
                "id": menu_item["id"],
                "name": menu_item["name"],
                "price": menu_item["price"],
                "quantity": quantity,
                "total": menu_item["price"] * quantity
            })
            total_price += menu_item["price"] * quantity

    if not selected_items:
        return jsonify({"error": "No valid menu items selected"}), 400

    new_order = {
        "id": order_counter,
        "client_id": client_id,
        "items": selected_items,
        "total_price": total_price
    }
    orders.append(new_order)
    order_counter += 1

    return jsonify(new_order), 201


if __name__ == '__main__':
    app.run(debug=True)