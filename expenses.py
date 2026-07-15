import csv
from datetime import datetime
import sqlite3
from database import get_connection

def set_budget(user_id):
    try:
        budget = float(input("\nEnter your monthly budget limit: ₹"))
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET budget = ? WHERE id = ?", (budget, user_id))
        conn.commit()
        conn.close()
        print(f"\n[+] Monthly budget successfully set to ₹{budget}")
    except ValueError:
        print("\n[!] Invalid amount. Budget not updated.")

def add_expense(user_id):
    print("\n--- ADD EXPENSE ---")
    print("Select a category:")
    print("1. Food")
    print("2. Travel")
    print("3. Bills")
    print("4. Entertainment")
    print("5. Others")
    print("6. <-- Go Back to Dashboard")
    
    cat_choice = input("Select an option (1-6): ")
    
    # Map numbers to category names
    categories = {
        '1': 'Food',
        '2': 'Travel',
        '3': 'Bills',
        '4': 'Entertainment',
        '5': 'Others'
    }
    
    # Check if user wants to go back
    if cat_choice == '6':
        print("\n[-] Action cancelled. Returning to dashboard...")
        return
        
    # Check if user made a valid selection
    if cat_choice in categories:
        category = categories[cat_choice]
    else:
        print("\n[!] Invalid choice. Returning to dashboard...")
        return

    # Proceed to take amount and description only after category is validated
    try:
        amount = float(input(f"Enter amount for {category} (₹): "))
    except ValueError:
        print("\n[!] Invalid amount type. Expense addition aborted.")
        return
        
    description = input("Enter description: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (user_id, date, category, amount, description) VALUES (?, ?, ?, ?, ?)", 
                   (user_id, date, category, amount, description))
    conn.commit()
    
    # Budget Monitoring Check
    cursor.execute("SELECT budget FROM users WHERE id = ?", (user_id,))
    budget = cursor.fetchone()[0]
    
    current_month = datetime.now().strftime("%Y-%m")
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date LIKE ?", (user_id, f"{current_month}%"))
    total_spent = cursor.fetchone()[0] or 0.0
    
    conn.close()
    
    print("\n[+] Expense added successfully!")
    if budget > 0:
        if total_spent > budget:
            print(f"\n[!] ALERT: You have exceeded your monthly budget of ₹{budget}! (Total spent: ₹{total_spent})")
        else:
            print(f"[i] Remaining monthly budget: ₹{budget - total_spent}")

def view_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date, category, amount, description FROM expenses WHERE user_id = ? ORDER BY date DESC", (user_id,))
    records = cursor.fetchall()
    conn.close()

    print("\n--- YOUR EXPENSES ---")
    if not records:
        print("No expenses found.")
    else:
        print(f"{'Date':<20} | {'Category':<15} | {'Amount':<10} | {'Description'}")
        print("-" * 70)
        for row in records:
            print(f"{row[0]:<20} | {row[1]:<15} | ₹{row[2]:<9} | {row[3]}")

def clear_records(user_id):
    confirm = input("\nAre you sure you want to delete ALL your expense records? (yes/no): ")
    if confirm.lower() == 'yes':
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        print("\n[+] All expense records cleared.")
    else:
        print("\n[-] Action cancelled.")

def export_csv(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date, category, amount, description FROM expenses WHERE user_id = ? ORDER BY date DESC", (user_id,))
    records = cursor.fetchall()
    conn.close()

    if not records:
        print("\n[!] No records to export.")
        return

    filename = f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])
        writer.writerows(records)
    
    print(f"\n[+] Data successfully exported to {filename}")