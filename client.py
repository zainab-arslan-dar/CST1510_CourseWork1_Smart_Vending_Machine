# Client Code
import socket


def display_menu():
    print("\nOptions:")
    print("1. View Products")
    print("2. Add to Cart")
    print("3. View Cart")
    print("4. Checkout")
    print("5. Exit")


def user_interface():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Created a socket to connect to the server.
    client.connect(('localhost', 1001)) # Connected to the server at localhost.

#Confirm the connection to the server
    print("Connected to the server.")

    while True:
        display_menu() # I display the menu options to the user.
        choice = input("Enter your choice (1-5): ").strip() #Ask for the user's choice.

        if choice == "1":  # View Products
            client.send("VIEW".encode('utf-8'))  # I send the 'VIEW' command to the server.
            response = client.recv(1024).decode('utf-8')  # I receive the list of products from the server.
            print(response)

        elif choice == "2":  # Add to Cart
            product_id = input("Enter Product ID: ").strip()
            quantity = input("Enter Quantity: ").strip()
            client.send(f"ADD,{product_id},{quantity}".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(response)

        elif choice == "3":  # View Cart
            client.send("VIEW-CART".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(response)

        elif choice == "4": #Checkout
            confirm_checkout = input("Proceed with checkout? (yes/no): ").strip().lower() #Ask the user for checkout Confirmatiom
            if confirm_checkout == "yes":
                client.send("CHECKOUT".encode('utf-8'))
                response = client.recv(1024).decode('utf-8')
                print(response)
            else:
                print("Checkout cancelled.")

        elif choice == "5":  # Exit
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    client.close()


user_interface()
