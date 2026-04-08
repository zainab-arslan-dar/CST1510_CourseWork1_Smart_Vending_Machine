import socket
import sqlite3
from datetime import datetime

# Connected to the SQLite database "shop.db" created in shopping_system_SQL file.
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# Function to load inventory from the database
def load_inventory():
    # Loaded all the products from the database and return them as a dictionary.
    cursor.execute("SELECT productID, productName, price, stock FROM products")
    return {row[0]: {"name": row[1], "price": row[2], "stock": row[3]} for row in cursor.fetchall()}

# Function to update the inventory in the database after a purchase
def update_inventory(product_id, quantity):
    # I updated the stock of a product in the database after a purchase is made.
    cursor.execute("UPDATE products SET stock = stock - ? WHERE productID = ?", (quantity, product_id))
    conn.commit()

# Function to save a transaction to the database
def save_transaction(cart):
    # Saving the details of the user's purchases into the transactions table.
    for product_id, details in cart.items():
        total_price = details["quantity"] * details["price"]
        cursor.execute(
            """
            INSERT INTO transactions (productID, quantity, totalPrice, transactionDate)
            VALUES (?, ?, ?, ?)
            """,
            (product_id, details["quantity"], total_price, datetime.now()),
        )
    conn.commit()

# Server function to handle client requests
def handle_client(client_socket):
    cart = {}  # I use this dictionary to track the user's current cart.
    inventory = load_inventory()  # I load the current inventory from the database.

    while True:
        try:
            # Receive the client's request and remove any extra whitespace.
            request = client_socket.recv(1024).decode("utf-8").strip()
            if not request:
                break

            if request == "VIEW":
                # Formats and sends the list of products to the client.
                response = "\n".join([
                    f"ID: {prod_id}, Name: {details['name']}, Price: ${details['price']:.2f}, Stock: {details['stock']}"
                    for prod_id, details in inventory.items()
                ])
                client_socket.send(response.encode("utf-8"))

            elif request.startswith("ADD"):
                # Handles adding a product to the cart.
                _, product_id, quantity = request.split(",")
                product_id = int(product_id)
                quantity = int(quantity)

                if product_id in inventory:
                    product = inventory[product_id]
                    if quantity <= product["stock"]:
                        if product_id not in cart:
                            # Add the product to the cart if it's not already there.
                            cart[product_id] = {
                                "name": product["name"],
                                "price": product["price"],
                                "quantity": quantity,
                            }
                        else:
                            # Updates the quantity if the product is already in the cart.
                            cart[product_id]["quantity"] += quantity

                        response = f"Added {quantity} of {product['name']} to the cart."
                    else:
                        response = f"Insufficient stock for {product['name']}. Only {product['stock']} available."
                else:
                    response = "Invalid Product ID."
                client_socket.send(response.encode("utf-8"))

            elif request == "VIEW-CART":
                # Formats the cart details for the client.
                if cart:
                    cart_lines = [
                        f"{details['name']} - ${details['price']:.2f} x {details['quantity']} = ${details['price'] * details['quantity']:.2f}"
                        for details in cart.values()
                    ]
                    total = sum(details['price'] * details['quantity'] for details in cart.values())
                    response = "Shopping Cart:\n" + "\n".join(cart_lines) + f"\nTotal: ${total:.2f}"
                else:
                    response = "Your cart is empty."
                client_socket.send(response.encode("utf-8"))

            elif request == "CHECKOUT":
                # Handles the checkout process, saving transactions and updating the inventory.
                if cart:
                    save_transaction(cart)  # Save the transaction details in the database.
                    for product_id, details in cart.items():
                        update_inventory(product_id, details["quantity"])  # Update the stock in the inventory.

                    cart_summary = "\n".join([
                        f"{details['name']} - ${details['price']:.2f} x {details['quantity']} = ${details['price'] * details['quantity']:.2f}"
                        for details in cart.values()
                    ])
                    total = sum(details['price'] * details['quantity'] for details in cart.values())
                    cart.clear()  # Clear the cart after checkout.
                    inventory = load_inventory()  # Reload the inventory to reflect updated stock.

                    response = cart_summary + f"\nTotal: ${total:.2f}\nCheckout successful! Thank you for shopping."
                else:
                    response = "Your cart is empty. Add items before checking out."
                client_socket.send(response.encode("utf-8"))

            else:
                # Inform the client if their request is invalid.
                response = "Invalid request."
                client_socket.send(response.encode("utf-8"))

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    client_socket.close()

# Start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 1001))
server.listen(5)
print("Waiting for connection...")

# Accept and handles the client
while True:
    client_socket, addr = server.accept()
    print(f"Connected by {addr}")
    handle_client(client_socket)

# Close the database connection.
conn.close()
