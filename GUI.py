import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('shop.db')
    return conn

# Product inventory details with products' pictures/logos, to make the GUI more interactive and user-friendly.
inventory = [
    {"id": 1, "product_name": "Harry Potter Series by J.K. Rowling", "price": 8.0, "stock": 40, "logo": 'Harrypotter_logo.png'},
    {"id": 2, "product_name": "It Ends With Us", "price": 11.0, "stock": 15, "logo": 'it_ends_with_us_logo.jpeg'},
    {"id": 3, "product_name": "The Call of the Wild", "price": 7.0, "stock": 20, "logo": 'the_call_of_wild_logo.jpg'},
    {"id": 4, "product_name": "The Lord of Rings", "price": 9.0, "stock": 15, "logo": 'the_lord_of rings_logo.png'},
    {"id": 5, "product_name": "Adobe Illustrator", "price": 30.0, "stock": 20, "logo": 'adobe-Illustrator-logo.png'},
    {"id": 6, "product_name": "Adobe Photoshop", "price": 50.0, "stock": 35, "logo": 'adobe-photoshop-logo.png'},
    {"id": 7, "product_name": "THE COOKBOOK By Martha Stewart", "price": 25.0, "stock": 45, "logo": 'cookbook_logo.jpeg'},
    {"id": 8, "product_name": "Wondershare Filmora", "price": 40.0, "stock": 35, "logo": 'Wondershare_logo.png'},
    {"id": 9, "product_name": "Starzplay Premium Annual Subscription", "price": 35.0, "stock": 20, "logo": 'starzplay-logo.png'},
    {"id": 10, "product_name": "Disney+ Subscription", "price": 30.0, "stock": 25, "logo": 'disney+logo.png'},
]

# Created an empty list cart.
cart = {}

# Created update_inventory_file function to update the stock in the inventory.txt file once the user purchases the product.
def update_inventory_file():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Update the stock for each product in the database
    for product in inventory:
        cursor.execute('''
            UPDATE products
            SET stock = ?
            WHERE productID = ?
        ''', (product['stock'], product['id']))
    conn.commit()
    cursor.close()
    conn.close()

# Created a function to record the transactions.
def record_transaction(product_id, product_name, quantity, total_price):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert the transaction into the database
    cursor.execute('''
        INSERT INTO transactions (productID, quantity, totalPrice)
        VALUES (?, ?, ?)
    ''', (product_id, quantity, total_price))
    conn.commit()
    cursor.close()
    conn.close()

# Defined the function to add products to cart.
def add_to_cart(product_id):
    for product in inventory:
        if product['id'] == product_id:
            if product_id not in cart:
                # If the product is not in the cart yet, add it with a quantity of 1
                cart[product_id] = {'product': product, 'quantity': 1}
            else:
                if cart[product_id]['quantity'] < product['stock']:
                    cart[product_id]['quantity'] += 1
                else:
                    # If the product is already in the cart, the quantity increases if stock allows
                    messagebox.showerror("Stock Error", f"Only {product['stock']} items available.")
                    return

            # Update stock in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products
                SET stock = ?
                WHERE productID = ?
            ''', (product['stock'] - cart[product_id]['quantity'], product_id))
            conn.commit()
            cursor.close()
            conn.close()

            update_cart_summary()
            break


# This function updates the cart summary every time a product is added.
def update_cart_summary():
    cart_text.delete(1.0, tk.END)
    total_cost = 0
    # I loop through the cart and display each product's details
    for item in cart.values():
        product = item['product']
        quantity = item['quantity']
        cost = quantity * product['price']
        total_cost += cost
        cart_text.insert(tk.END, f"{product['product_name']} - {quantity} x ${product['price']} = ${cost}\n")
    cart_text.insert(tk.END, f"\nTotal: ${total_cost:.2f}")

# This function handles the checkout process after the user is ready to buy
def proceed_to_checkout():
    total_cost = sum(item['quantity'] * item['product']['price'] for item in cart.values())
    response = messagebox.askyesno("Confirm Checkout", f"Total cost is ${total_cost:.2f}. Proceed?")
    if response:
        confirm_checkout(total_cost)

# This function processes the actual checkout: updates inventory and records the transaction
def confirm_checkout(total_cost):
    conn = get_db_connection()
    cursor = conn.cursor()

    for item in cart.values():
        product = item['product']
        quantity = item['quantity']
        total_price = quantity * product['price']

        # Insert the transaction into the database
        cursor.execute('''
            INSERT INTO transactions (productID, quantity, totalPrice)
            VALUES (?, ?, ?)
        ''', (product['id'], quantity, total_price))

        # Update product stock
        new_stock = product['stock'] - quantity
        cursor.execute('''
            UPDATE products
            SET stock = ?
            WHERE productID = ?
        ''', (new_stock, product['id']))

        # Update the inventory in the in-memory list
        product['stock'] = new_stock

    conn.commit()
    cursor.close()
    conn.close()

    # Clear cart and update cart summary
    cart.clear()
    update_cart_summary()
    messagebox.showinfo("Checkout Successful", f"Thank you for your purchase! Total: ${total_cost:.2f}")


# Main application window
root = tk.Tk()
root.title("Smart Vending Machine")
root.configure(bg="#FFFFFF")

# Set up the layout of the GUI with a split screen: product listing on the left, cart summary on the right
main_frame = tk.Frame(root, bg="#FFFFFF")
main_frame.pack(fill=tk.BOTH, expand=True)

# Left side of product listing frame
product_frame = tk.Frame(main_frame, bg="#FFFFFF")
product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

product_label = tk.Label(product_frame, text="Available Products", font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#333")
product_label.pack(pady=10)

images = []  # List to keep references to images
for product in inventory:
    product_info = f"{product['product_name']} - ${product['price']} - Stock: {product['stock']}"

    product_item_frame = tk.Frame(product_frame, bg="#FFFFFF")
    product_item_frame.pack(fill=tk.X, pady=5)

    # Load and display product image to fit to layout
    try:
        img = Image.open(product['logo'])
        img = img.resize((50, 50))  # Resize the image to a smaller size
        img = ImageTk.PhotoImage(img)
        images.append(img)  # Keep reference to avoid garbage collection
        img_label = tk.Label(product_item_frame, image=img, bg="#FFFFFF")
        img_label.pack(side=tk.LEFT, padx=10)
    except Exception as e:
        print(f"Error loading image for {product['product_name']}: {e}")

    product_label = tk.Label(product_item_frame, text=product_info, font=("Georgia", 12), bg="#FFFFFF", fg="#333")
    product_label.pack(side=tk.LEFT, padx=10)

    # Add a button to each product to add it to the cart
    add_button = tk.Button(product_item_frame, text="Add to Cart", command=lambda p_id=product['id']: add_to_cart(p_id),
                           font=("Arial", 10), bg="#008000", fg="white", activebackground="#45a049", padx=10, pady=5)
    add_button.pack(side=tk.RIGHT, padx=10)

# Right side for cart summary with a scrollbar
cart_frame = tk.Frame(main_frame, bg="#f5f5f5", bd=2, relief="groove")
cart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

cart_label = tk.Label(cart_frame, text="Your Cart Summary", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333")
cart_label.pack()

cart_text_frame = tk.Frame(cart_frame, bg="#f5f5f5")
cart_text_frame.pack(fill=tk.BOTH, expand=True)

cart_text = tk.Text(cart_text_frame, height=20, font=("Arial", 12), bg="#ffffff", fg="#333", wrap=tk.WORD)
cart_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

cart_scrollbar = tk.Scrollbar(cart_text_frame, command=cart_text.yview)
cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

cart_text.config(yscrollcommand=cart_scrollbar.set)

# Button to proceed to checkout
checkout_button = tk.Button(cart_frame, text="Proceed to Checkout", command=proceed_to_checkout,
                             font=("Arial", 12, "bold"), bg="#2196f3", fg="white", activebackground="#1976d2", padx=20, pady=10)
checkout_button.pack(pady=10)

# Start the main loop for the tkinter application to run the interface
root.mainloop()
