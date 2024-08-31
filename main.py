from content_factory import create_outlines, create_articles, add_meta_descriptions, create_introductions

def display_menu():
    print("\n--- Content Factory Menu ---")
    print("1. Create Outlines")
    print("2. Create Articles (including introductions)")
    print("3. Add Meta Descriptions")
    print("4. Create Introductions Only")
    print("0. Exit")
    return input("Enter your choice: ")

def main():
    while True:
        choice = display_menu()
        if choice == "1":
            create_outlines()
        elif choice == "2":
            create_articles()
        elif choice == "3":
            add_meta_descriptions()
        elif choice == "4":
            create_introductions()
        elif choice == "0":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
