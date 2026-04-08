import os
def load_inventory():
    inventory = {}
    with open('inventory.txt', "r") as file:
        data = file.readlines()
        keys = data[0].strip().split(',')
        for k in keys:
            inventory[k] = []
        for line in data[1:]:
            values = [v.strip() for v in line.strip().split(',')]  # Strip extra spaces
            for k, v in zip(keys, values):
                inventory[k].append(v)

    return inventory
class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def update_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False


class Cart:
    def __init__(self):
        self.items = {}  # Dictionary to store product ID and quantities

    def add_item(self, product, quantity):
        if product.update_stock(quantity):
            if product.product_id in self.items:
                self.items[product.product_id]['quantity'] += quantity
            else:
                self.items[product.product_id] = {
                    'product': product,
                    'quantity': quantity,
                }
            print(f"Added {quantity} of {product.name} to the cart.")
        else:
            print(f"Insufficient stock for {product.name}.")

    def view_items(self):
        result = "\nShopping Cart:\n"
        total_cost = 0
        for item in self.items.values():
            product = item['product']
            quantity = item['quantity']
            cost = quantity * product.price
            result += f"{product.name} - ${product.price:.2f} x {quantity} = ${cost:.2f}\n"
            total_cost += cost
        result += f"Total: ${total_cost:.2f}\n"
        return result

    def clear_cart(self):
        self.items.clear()


class VendingMachine:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        self.inventory = {}  # Dictionary to store Product objects
        self.cart = Cart()

    def load_inventory(self):
        with open(self.inventory_file, "r") as file:
            data = file.readlines()
            keys = data[0].strip().split(',')
            for line in data[1:]:
                values = [v.strip() for v in line.strip().split(',')]
                product = Product(
                    product_id=values[0],
                    name=values[1],
                    price=values[2],
                    stock=values[3],
                )
                self.inventory[product.product_id] = product

    def view_products(self):
        result = "\nAvailable Products:\n"
        for product in self.inventory.values():
            result += (f"ID: {product.product_id} - {product.name} "
                       f"- ${product.price:.2f} - Stock: {product.stock}\n")
        return result

    def save_inventory(self):
        with open(self.inventory_file, "w") as file:
            file.write("id,product_name,price,stock\n")
            for product in self.inventory.values():
                file.write(f"{product.product_id},{product.name},{product.price},{product.stock}\n")

    def save_transaction(self):
        file_exists = os.path.exists("transaction.txt")
        with open("transaction.txt", "a") as file:
            if not file_exists:
                file.write("transaction_id,product_id,quantity,total_price\n")
            for item in self.cart.items.values():
                product = item['product']
                quantity = item['quantity']
                file.write(f"{product.product_id},{product.name},{product.price},{quantity}\n")

    def checkout(self):
        if self.cart.items:
            print("\nCheckout Summary:")
            print(self.cart.view_items())
            confirm_checkout = input("Proceed with checkout? (y/n): ").strip().lower()
            if confirm_checkout == "y":
                self.save_transaction()
                self.save_inventory()
                self.cart.clear_cart()
                print("Thank you for shopping with us!")
            else:
                print("Checkout cancelled.")
        else:
            print("\nYour cart is empty. Add items before checking out.")

    def menu(self):
        self.load_inventory()
        print("\nWelcome to the Smart Vending Machine!")
        while True:
            print("\nPlease choose an option:")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Checkout")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ").strip()
            if choice == "1":
                print(self.view_products())
            elif choice == "2":
                product_id = input("Enter product ID: ").strip()
                quantity = int(input("Enter quantity: ").strip())
                if product_id in self.inventory:
                    self.cart.add_item(self.inventory[product_id], quantity)
                else:
                    print("Invalid Product ID.")
            elif choice == "3":
                print(self.cart.view_items())
            elif choice == "4":
                self.checkout()
            elif choice == '5':
                print("Thank you for shopping with us! Goodbye.")  # Exit the loop and end the program
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")
                break


# Run the program
vending_machine = VendingMachine("inventory.txt")
vending_machine.menu()
