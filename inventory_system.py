import json
import logging
from datetime import datetime

# Configure logging properly
logging.basicConfig(
    filename="inventory_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global variable to hold inventory data
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add an item to the inventory with validation.

    Args:
        item (str): Name of the item.
        qty (int): Quantity to add.
        logs (list, optional): List to store log entries.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str):
        logging.error(f"Invalid item name type: {type(item)}. Must be a string.")
        return
    if not isinstance(qty, int):
        logging.error(f"Invalid quantity type: {type(qty)}. Must be an integer.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info(f"Added {qty} of {item}")


def remove_item(item, qty):
    """
    Remove a specific quantity of an item from inventory.

    Args:
        item (str): Name of the item.
        qty (int): Quantity to remove.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info(f"Removed {item} completely from stock.")
        else:
            logging.info(f"Removed {qty} of {item}. Remaining: {stock_data[item]}")
    except KeyError as e:
        logging.warning(f"Attempted to remove non-existent item: {item}. Error: {e}")


def get_qty(item):
    """
    Get the current quantity of a given item.

    Args:
        item (str): Name of the item.

    Returns:
        int: Quantity of the item.
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from a JSON file.

    Args:
        file (str): File path to load data from.
    """
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
            logging.info("Loaded inventory data from file.")
    except FileNotFoundError:
        logging.warning(f"{file} not found. Starting with empty inventory.")


def save_data(file="inventory.json"):
    """
    Save the current inventory data to a JSON file.

    Args:
        file (str): File path to save data.
    """
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)
        logging.info("Saved inventory data to file.")


def print_data():
    """Print the current inventory data."""
    logging.info("Generating inventory report...")
    print("Items Report:")
    for i in stock_data:
        print(f"{i} -> {stock_data[i]}")


def check_low_items(threshold=5):
    """
    Check for items with quantity below a given threshold.

    Args:
        threshold (int): Minimum stock level before alert.

    Returns:
        list: Items that are below the threshold.
    """
    return [i for i, q in stock_data.items() if q < threshold]


def main():
    """Main execution block for inventory management."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types — now logged as errors
    remove_item("apple", 3)
    remove_item("orange", 1)
    logging.info(f"Apple stock: {get_qty('apple')}")
    logging.info(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()
    logging.info("Program execution completed successfully.")


if __name__ == "__main__":
    main()
