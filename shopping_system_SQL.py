import sqlite3


#Creates the database shop.db and populates it with two tables.
def create_and_populate_database():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

#Creates a table named "products" with relevant headings.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        productID INTEGER PRIMARY KEY AUTOINCREMENT,
        productName TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

#Creates a table named "transactions" with relevant headings.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        productID INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        totalPrice REAL NOT NULL,
        transactionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (productID) REFERENCES products(productID)
    )
    """)

#Fills the following product data in the products table created in the database.
    products = [
        (1, 'Harry Potter Series by J.K. Rowling', 8.0, 40),
        (2, 'It Ends With Us', 11.0, 13),
        (3, 'The Call of the Wild', 7.0, 19),
        (4, 'The Lord of Rings', 9.0, 15),
        (5, 'Adobe Illustrator', 30.0, 20),
        (6, 'Adobe Photoshop', 50.0, 35),
        (7, 'The Cookbook by Martha Stewart', 25.0, 45),
        (8, 'Wondershare Filmora', 40.0, 35),
        (9, 'Starzplay Premium Annual Subscription', 35.0, 20),
        (10, 'Disney+ Subscription', 30.0, 25),
    ]


    cursor.executemany("""
    INSERT OR IGNORE INTO products (productID, productName, price, stock)
    VALUES (?, ?, ?, ?)
    """, products)

    conn.commit()
    cursor.close()
    conn.close()

#Call the function to create the database and populate it with product data.
create_and_populate_database()

