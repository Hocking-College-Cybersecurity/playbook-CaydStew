# ----------------------------------------
# List Manager Application
# ----------------------------------------

# Empty list
items = []

# Shows all items using a loop
def display_items():
    print("\n--- Current Items ---")
    if not items:
        print("The list is empty.")
    else:
        # Loop through each item in the list
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item}")
    print("---\n")

# Menu loop runs until users choose to exit
while True:
    # Show menu options
    print("Choose an option:")
    print("1. Show an item")
    print("2. Create an item")
    print("3. Remove items")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ").strip()

    # Check if choice is 1–4
    if choice not in ["1", "2", "3", "4"]:
        print("Enter a number from 1 to 4.\n")
        continue

    # Option 1: Show an item
    if choice == "1":
        if not items:
            print("List Empty.\n")
        else:
            index = input("Enter the item number to show: ").strip()
            if index.isdigit() and 1 <= int(index) <= len(items):
                print(f"Item {index}: {items[int(index) - 1]}\n")
            else:
                print("Invalid item number.\n")

    # Option 2: Add an item
    elif choice == "2":
        new_item = input("Enter an item to add: ").strip()
        if new_item:           # make sure it's not empty
            items.append(new_item)
            print(f"'{new_item}' added successfully!\n")
        else:
            print("Item cannot be empty.\n")
        # Added item. Returning to main menu.

    # Option 3: Remove items
    elif choice == "3":
        if not items:
            print("List is empty.\n")
            continue

        # Show all items and ask for the item number to remove
        display_items()
        index = input("Enter the item number to remove: ").strip()

        # Make sure the input is a number and within range
        if index.isdigit() and 1 <= int(index) <= len(items):
            removed = items.pop(int(index) - 1)
            print(f"Removed '{removed}'.\n")
        else:
            print("Invalid item number.\n")

    # Option 4: Exit program
    elif choice == "4":
        print("Have a good day! Goodbye!")
        break