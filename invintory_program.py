import sqlite3
import os


DATABASE_NAME = "inventory.db"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def connect_to_database():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection


def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            item_type TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_item():
    name = input("Enter item name: ")
    item_type = input("Enter item type: ")

    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO inventory (name, item_type)
        VALUES (?, ?)
    """, (name, item_type))

    connection.commit()
    connection.close()

    print("Item added successfully!")


def view_inventory():
    clear_screen()
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    connection.close()

    if len(items) == 0:
        print("Your inventory is empty.")
        return

    print("\nInventory:")
    for item in items:
        print(f"ID: {item[0]} | Name: {item[1]} | Type: {item[2]}")

    selected_id = input("\nEnter the ID of an item to edit/remove, or press Enter to go back: ")

    if selected_id == "":
        return

    item_menu(selected_id)


def item_menu(item_id):
    while True:
        clear_screen()
        print("\nWhat would you like to do?")
        print("1. Edit item")
        print("2. Remove item")
        print("3. Go back")

        choice = input("Choose an option: ")

        if choice == "1":
            edit_item(item_id)
            break
        elif choice == "2":
            remove_item(item_id)
            break
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


def edit_item(item_id):
    new_name = input("Enter new item name: ")
    new_type = input("Enter new item type: ")

    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE inventory
        SET name = ?, item_type = ?
        WHERE id = ?
    """, (new_name, new_type, item_id))

    connection.commit()
    connection.close()

    print("Item updated successfully!")


def remove_item(item_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM inventory
        WHERE id = ?
    """, (item_id,))

    connection.commit()
    connection.close()

    print("Item removed successfully!")


def main_menu():
    while True:
        clear_screen()
        print("\nInventory Program")
        print("1. New item")
        print("2. Look at inventory")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_item()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


create_table()
main_menu()