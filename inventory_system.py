"""
Inventory Management System Module

This module provides functionality to manage an inventory,
including adding, removing, saving, loading, and checking low-stock items.
"""

import json
import logging
import os

# ================== LOGGER CONFIGURATION ==================
logging.basicConfig(
    filename="inventory.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode="a",
)

# ================== CONSTANTS ==================
LOW_STOCK_THRESHOLD = 5
DATA_FILE = "inventory_data.json"


# ================== ADD ITEM ==================
def add_item(item_name, quantity, price, inventory_data):
    """Add an item to the inventory."""
    if item_name in inventory_data:
        inventory_data[item_name]["quantity"] += quantity
        logging.info("Increased quantity for %s by %d", item_name, quantity)
    else:
        inventory_data[item_name] = {"quantity": quantity, "price": price}
        logging.info("Added new item %s with quantity %d", item_name, quantity)


# ================== REMOVE ITEM ==================
def remove_item(item_name, quantity, inventory_data):
    """Remove quantity of an item from the inventory."""
    if item_name not in inventory_data:
        logging.warning("Attempted to remove %s but item not found", item_name)
        return

    if inventory_data[item_name]["quantity"] < quantity:
        logging.warning(
            "Cannot remove %d of %s; only %d in stock",
            quantity,
            item_name,
            inventory_data[item_name]["quantity"],
        )
        return

    inventory_data[item_name]["quantity"] -= quantity
    logging.info("Removed %d of %s", quantity, item_name)

    if inventory_data[item_name]["quantity"] == 0:
        del inventory_data[item_name]
        logging.info("Item %s is now out of stock and removed", item_name)


# ================== GET QUANTITY ==================
def get_qty(item_name, inventory_data):
    """Get quantity of a specific item."""
    return inventory_data.get(item_name, {}).get("quantity", 0)


# ================== LOAD DATA ==================
def load_data():
    """Load inventory data from JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error("Error loading data from %s: %s", DATA_FILE, str(e))
            return {}
    logging.warning("No existing data file found at %s", DATA_FILE)
    return {}


# ================== SAVE DATA ==================
def save_data(inventory_data):
    """Save inventory data to JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(inventory_data, file, indent=4)
        logging.info("Inventory data saved successfully to %s", DATA_FILE)
    except (OSError, json.JSONDecodeError) as e:
        logging.error("Error saving inventory data: %s", str(e))


# ================== PRINT DATA ==================
def print_data(inventory_data):
    """Print all items in inventory."""
    if not inventory_data:
        print("Inventory is empty.")
        return

    print("Current Inventory:")
    for item, details in inventory_data.items():
        print(
            f"{item}: Quantity = {details['quantity']}, "
            f"Price = {details['price']}"
        )


# ================== CHECK LOW ITEMS ==================
def check_low_items(inventory_data):
    """Check and print items that are low in stock."""
    low_items = {
        item: details
        for item, details in inventory_data.items()
        if details["quantity"] < LOW_STOCK_THRESHOLD
    }

    if low_items:
        print("Low Stock Items:")
        for item, details in low_items.items():
            print(
                f"{item}: Quantity = {details['quantity']}, "
                f"Threshold = {LOW_STOCK_THRESHOLD}"
            )
            logging.warning(
                "Low stock alert for %s (Quantity: %d)",
                item,
                details["quantity"],
            )
    else:
        print("No low-stock items found.")


# ================== MAIN FUNCTION ==================
def main():
    """Main driver function for the inventory system."""
    inventory_data = load_data()

    while True:
        print("\n--- Inventory Management ---")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. View Quantity")
        print("4. View All Items")
        print("5. Check Low Stock")
        print("6. Save & Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter item name: ")
            qty = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            add_item(name, qty, price, inventory_data)

        elif choice == "2":
            name = input("Enter item name: ")
            qty = int(input("Enter quantity to remove: "))
            remove_item(name, qty, inventory_data)

        elif choice == "3":
            name = input("Enter item name: ")
            print(f"Quantity of {name}: {get_qty(name, inventory_data)}")

        elif choice == "4":
            print_data(inventory_data)

        elif choice == "5":
            check_low_items(inventory_data)

        elif choice == "6":
            save_data(inventory_data)
            print("Data saved. Exiting program.")
            break

        else:
            print("Invalid choice, try again.")


# ================== ENTRY POINT ==================
if __name__ == "__main__":
    main()
