import sqlite3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Function to establish a connection to the database
def establish_db_connection():
    conn = sqlite3.connect('shop.db')
    return conn


# Function to retrieve the current stock levels of products from the database
def get_current_stock():
    conn = establish_db_connection()
    cursor = conn.cursor()

    cursor.execute('''SELECT productID, productName, stock FROM products''')
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    product_names = [product[1] for product in products]
    product_stocks = [product[2] for product in products]

    return product_names, product_stocks


# Function to update the bar chart with real-time stock data
def refresh_stock_graph(frame, bars, product_names):
    product_names, product_stocks = get_current_stock()

    # Update the heights of the bars by modifying the 'Rectangle' objects
    for bar, stock in zip(bars, product_stocks):
        bar.set_height(stock)  # Update each bar's height with the new stock level

    return bars


# Function to generate the initial bar chart for stock distribution
def generate_stock_distribution_chart():
    product_names, product_stocks = get_current_stock()

    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a bar chart for stock distribution
    bars = ax.bar(product_names, product_stocks, color='green')

    ax.set_title('Real-Time Stock Distribution Graph')
    ax.set_xlabel('Products')
    ax.set_ylabel('Stock Level')

    # Set up real-time updating of the graph (animation)
    ani = FuncAnimation(
        fig,
        refresh_stock_graph,
        fargs=(bars, product_names),
        interval=1000,
        frames=None,  # If you want the animation to run indefinitely, you can leave this as None
        cache_frame_data=False  # Suppress caching warning
    )

    # Show the plot
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# Start the real-time graph
generate_stock_distribution_chart()

