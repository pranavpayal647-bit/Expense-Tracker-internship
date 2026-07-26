import database
import auth
import analytics
import csv_exporter
import pdf_export
import search
from rich.console import Console
from rich.table import Table

console = Console()

def get_input_or_back(prompt):
    val = input(prompt).strip()
    if val.lower() == 'back':
        return None
    return val

def run_dashboard(user_id, username):
    while True:
        console.print(f"\n[bold bright_yellow]--- DASHBOARD: {username.upper()} ---[/bold bright_yellow]")
        console.print("1. Add Expense\n2. Set Monthly Budget\n3. View Expenses & Current Overview\n4. Advanced Search\n5. View Visual Analytics\n6. Export CSV\n7. Export PDF\n8. Clear Expense History\n9. Logout")
        choice = input("Enter Choice (1-9) : ").strip()
        
        if choice == '1':
            item = get_input_or_back("Item Description : ")
            if item is None: continue
            
            console.print("Categories: 1. Food | 2. Travel | 3. Study | 4. Other")
            cat_choice = get_input_or_back("Select Category (1-4) : ")
            if cat_choice is None: continue
            cats = {"1": "Food", "2": "Travel", "3": "Study", "4": "Other"}
            cat = cats.get(cat_choice, "Other")
            
            amt_str = get_input_or_back("Amount (Rs) : ")
            if amt_str is None: continue
            
            try:
                amt = float(amt_str)
                database.add_expense(user_id, item, cat, amt)
                console.print("[green]✅ Expense added successfully![/green]")
                
                # Check for Budget Warning
                total = database.get_total_spent(user_id)
                limit = database.get_budget(user_id)
                if limit > 0 and total > limit:
                    console.print(f"[bold red]⚠️ WARNING: You have exceeded your monthly budget of Rs. {limit:,.2f}![/bold red]")
            except ValueError:
                console.print("[red]❌ Invalid Amount.[/red]")
            
        elif choice == '2':
            amt = get_input_or_back("New Budget Limit (Rs) : ")
            if amt: database.set_budget(user_id, float(amt))
            
        elif choice == '3':
            # Displaying Expenses in a Table
            expenses = database.get_all_expenses(user_id)
            table = Table(title=f"Expense Overview for {username}")
            table.add_column("Date", style="cyan")
            table.add_column("Description", style="magenta")
            table.add_column("Category", style="green")
            table.add_column("Amount", style="bold")
            
            for item, cat, amt, date in expenses:
                table.add_row(date, item, cat, f"Rs. {amt:,.2f}")
            
            console.print(table)
            
            total = database.get_total_spent(user_id)
            limit = database.get_budget(user_id)
            console.print(f"[bold]Total Spent: Rs. {total:,.2f} | Limit: Rs. {limit:,.2f}[/bold]")
            
        elif choice == '4':
            kw = get_input_or_back("Keyword to Search : ")
            if kw: search.execute_search(user_id, kw)
            
        elif choice == '5':
            analytics.display_budget_meter(user_id)
            analytics.display_category_breakdown(user_id)
            
        elif choice == '6':
            csv_exporter.export_to_csv(user_id, username)
        elif choice == '7':
            pdf_export.export_to_pdf(user_id, username)
        elif choice == '8':
            confirm = input("Are you sure you want to clear ALL expense history? (yes/no): ")
            if confirm.lower() == 'yes':
                database.clear_expenses(user_id)
                console.print("[bold red]All expenses cleared.[/bold red]")
        elif choice == '9':
            break

def main():
    database.init_db()
    console.print("[bold blue]--- PERSONAL EXPENSE TRACKER SYSTEM (PETS) ---[/bold blue]")
    choice = input("1. Register New Account\n2. Login to Dashboard\nChoice: ")
    
    if choice == '1':
        email = input("Email Address : ")
        if auth.verify_otp_flow(email):
            user = input("Username : ")
            pwd = input("Password : ")
            if database.register_user(user, pwd, email):
                console.print("[green]Registered! Please Login.[/green]")
            else:
                console.print("[red]User already exists.[/red]")
        else:
            console.print("[red]Verification failed.[/red]")
            return
            
    username = input("Username : ")
    password = input("Password : ")
    user_data = database.get_user(username)
    
    if user_data and user_data[2] == password:
        console.print("[green]✅ LOGIN SUCCESSFUL! Welcome back.[/green]")
        run_dashboard(user_data[0], user_data[1])
    else:
        console.print("[red]Invalid login.[/red]")

if __name__ == "__main__":
    main()