def load_inventory():
    # Read the entire file and split lines into a list
    with open('inventory.txt', "r") as file:
        lines = file.readlines()

    # Get the headers (keys) from the first line and initialize the dictionary
    keys = lines[0].strip().split(',')
    inventory = {key: [] for key in keys}

    # Process each line after the header and fill the inventory dictionary
    for line in lines[1:]:
        values = line.strip().split(',')
        for key, value in zip(keys, values):
            inventory[key].append(value.strip())

    return inventory


def view_products(inventory):
    result = '\nAvailable products:\n'
    for i in range(len(inventory['id'])):
            result += f"ID: {inventory['id'][i]} - {inventory['product_name'][i]} - ${float(inventory['price'][i]):.2f} - Stock: {inventory['stock'][i]}\n"
    return result


cart = {}

def add_to_cart(id, quantity, inventory):
    index =  inventory['id'].index(id)
    available_stock = int(inventory['stock'][index])

    if available_stock >= quantity:
        cart[id] ={
            'product_name': inventory['product_name'][index],
            'price': inventory['price'][index],
            'quantity': quantity,
        }

    inventory['stock'][index] = available_stock - quantity
    print(cart)


def view_cart(cart):
    result = '\nShopping Cart: \n'
    total = 0
    all_total = 0
    for id, item in cart.items():
        total = item['quantity'] * float(item['price'])
        result += f'{item["product_name"]} - ${item["price"]} x {item["quantity"]} = ${total}\n'
    all_total += total
    result += f'Total: ${all_total}\n'
    return result


def save_cart(cart):
    result = '\nid,product_name,price,stock \n'
    for id, item in cart.items():
        result += f'{id}, {item["product_name"]}, {item["price"]}, {item["quantity"]}\n'
    with open('cart.txt', 'w') as file:
        file.write(result)
save_cart(cart)

def save_inventory(inventory):
    result = 'id,product_name,price,stock\n'
    for i in range(len(inventory['id'])):
        result += f"{inventory['id'][i]},{inventory['product_name'][i]},{inventory['price'][i]},{inventory['stock'][i]}\n"
    with open('inventory.txt', 'w') as file:
        file.write(result)

def save_transaction(cart):
    with open('transactions.txt', 'a') as file:
        for id, item in cart.items():
            file.write(f"Product: {item['product_name']} - Quantity: {item['quantity']} - Price: ${item['price']} each\n")
        total_cost = sum(item['quantity'] * float(item['price']) for item in cart.values())
        file.write(f"Total Cost: ${total_cost}\n")
        file.write('-' * 40 + '\n')

def checkout(msg, inventory):
    result = ''
    if msg == 'yes':
        print("\nCheckout Confirmation:")
        total_cost = 0
        for id, item in cart.items():
            total_cost += item['quantity'] * float(item['price'])
            print(
                f"{item['product_name']} - ${item['price']} x {item['quantity']} = ${item['quantity'] * float(item['price'])}")
        print(f"\nTotal Cost: ${total_cost}")
        save_cart(cart)
        #save inventory
        save_inventory(inventory)
        # Log the transaction
        save_transaction(cart)
        #clear cart
        cart.clear()
        result = ('Thank you for shopping with us!')
    else:
        result = ('Checkout cancelled')
    return result

def menu():
    inventory = load_inventory()
    print('\nWelcome to the Smart Vending Machine')
    while True:
        # Display the menu options
        print("\nPlease choose an option:")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Exit")

        # Get the user’s choice
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            print(view_products(inventory))  # Display available products
        elif choice == '2':
           id = input("Enter product ID: ")
           quantity = int(input("Enter quantity: "))
           add_to_cart(id, quantity, inventory)
        elif choice == '3':
            print(view_cart(cart)) # Display items in the cart
        elif choice == '4':
            checkout_choice = input('Would you like to checkout? (yes/no): ')
            print(checkout(checkout_choice, inventory)) # Proceed with checkout
        elif choice == '5':
            print("Thank you for shopping with us! Goodbye.") # Exit the loop and end the program
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")
            break
 menu()
