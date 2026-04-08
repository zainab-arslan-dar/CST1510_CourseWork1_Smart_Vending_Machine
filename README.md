# CST1510_CourseWork1_Smart_Vending_Machine
Smart Vending Machine project with a Tkinter GUI, SQLite database, and client-server architecture. Users can browse products, add to cart, view cart summary, and checkout. Inventory and transactions are tracked in real-time, demonstrating Python GUI, database management, and network programming in a practical, interactive system.
# Smart Vending Machine

This project implements a **Smart Vending Machine** using Python, SQLite, and socket programming. The system provides a user-friendly interface for browsing products, managing a shopping cart, and completing transactions. It includes server-client communication and persistent storage using a database.

---

## Features

- Browse available products with real-time stock information.
- Add products to a shopping cart with quantity control.
- View cart in a clean, organized format with total cost.
- Checkout process updates inventory and records transactions.
- Persistent storage using SQLite database (`shop.db`).
- Server-client architecture using Python sockets for networked operations.

---

## Folder Structure
SmartVendingMachine/
│
├── server.py # Server code handling inventory and client requests
├── client.py # Client code for user interface and interaction
├── shop.db # SQLite database storing products and transactions
├── database_setup.py # Script to create and populate the database
├── images/ # Product images/logos
└── README.md # Project documentation


---

## Prerequisites

- Python 3.x
- SQLite3 (usually comes with Python)
- PIL (Python Imaging Library) for product images:
  bash
pip install pillow


---

## Setup Instructions

1. **Clone the repository**
git clone https://github.com/your-username/SmartVendingMachine.git
cd SmartVendingMachine

3. **Install required packages**
pip install pillow

5. **Set up the database**
python database_setup.py
This will create shop.db and populate it with initial products.

4. **Start the server**
python server.py
The server will start listening on localhost:1001.

5. **Run the client**
python client.py
