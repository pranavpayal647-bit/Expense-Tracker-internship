from database import init_db
from auth import sign_up, login
from expenses import add_expense, view_expenses, set_budget, export_csv, clear_records

def main():
    # Initialize the database when the program starts
    init_db()
    
    while True:
        print("\n=== EXPENSE TRACKER SYSTEM ===")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            sign_up()
        elif choice == '2':
            user_id = login()
            if user_id:
                # Post-login Dashboard Menu
                while True:
                    print("\n--- DASHBOARD ---")
                    print("1. Add Expense")
                    print("2. View Expenses")
                    print("3. Set Monthly Budget")
                    print("4. Export to CSV")
                    print("5. Clear All Records")
                    print("6. Logout")
                    
                    sub_choice = input("Select an option: ")
                    
                    if sub_choice == '1':
                        add_expense(user_id)
                    elif sub_choice == '2':
                        view_expenses(user_id)
                    elif sub_choice == '3':
                        set_budget(user_id)
                    elif sub_choice == '4':
                        export_csv(user_id)
                    elif sub_choice == '5':
                        clear_records(user_id)
                    elif sub_choice == '6':
                        print("\nLogging out...")
                        break
                    else:
                        print("\n[!] Invalid choice.")
        elif choice == '3':
            print("\nExiting system. Goodbye!")
            break
        else:
            print("\n[!] Invalid choice.")

if __name__ == "__main__":
    main()