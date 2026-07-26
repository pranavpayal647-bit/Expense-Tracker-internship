from rich.console import Console
from rich.table import Table
import database

console = Console()

def execute_search(user_id, keyword):
    all_exp = database.get_all_expenses(user_id)
    # Searching item name or category
    results = [e for e in all_exp if keyword.lower() in e[0].lower() or keyword.lower() in e[1].lower()]
    
    table = Table(title=f"Search Results for '{keyword}'")
    table.add_column("Date", style="cyan")
    table.add_column("Item", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Amount", style="bold")
    
    for row in results:
        table.add_row(row[3], row[0], row[1], str(row[2]))
    
    console.print(table)