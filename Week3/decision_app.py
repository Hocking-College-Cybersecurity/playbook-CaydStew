def main():
    while True:
        print("\n--- Decisions ---")
        q1 = input("Do you like to go to bed late? (yes/no): ").strip().lower()
        q2 = input("Do you like muffins? (yes/no): ").strip().lower()
        q3 = input("Is winter the best season? (yes/no): ").strip().lower()
        q4 = input("Is ice cream the best dessert? (yes/no): ").strip().lower()

        print("\n--- Result ---")
        again = input("Would you like to answer again? (yes/no): ").strip().lower()
        if again != "yes":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()