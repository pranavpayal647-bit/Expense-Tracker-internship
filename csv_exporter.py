import csv
from rich.console import Console
import database

console = Console()

def export_to_csv(user_id: int, username: str):
    data = database.get_all_expenses(user_id)
    filename = f"{username}_report.csv"
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Item', 'Category', 'Amount', 'Date'])
            writer.writerows(data)
        console.print(f"[bold green]✅ Exported to {filename}[/bold green]")
    except Exception as e:
        console.print(f"[red]Error exporting CSV: {e}[/red]")