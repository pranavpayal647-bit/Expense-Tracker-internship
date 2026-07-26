from rich.console import Console
from rich.panel import Panel
import database

console = Console()

def display_budget_meter(user_id: int):
    total_spent = database.get_total_spent(user_id)
    budget_limit = database.get_budget(user_id)

    if budget_limit <= 0:
        console.print("[yellow]Set a budget to see progress.[/yellow]")
        return

    percentage = (total_spent / budget_limit) * 100
    bar_length = 20
    filled = int(bar_length * min(percentage, 100) // 100)
    progress_bar = "█" * filled + "░" * (bar_length - filled)

    console.print(Panel(
        f"Usage: [{progress_bar}] {percentage:.1f}%\n"
        f"Spent: Rs.{total_spent:,.2f} / Rs.{budget_limit:,.2f}",
        title="Budget Progress"
    ))

def display_category_breakdown(user_id: int):
    totals = database.get_category_totals(user_id)
    if not totals:
        console.print("[yellow]No expenses found to analyze.[/yellow]")
        return

    # Color mapping for different categories
    colors = {"Food": "green", "Travel": "blue", "Study": "cyan", "Other": "white"}
    
    console.print("\n[bold]Category Analytics:[/bold]")
    for cat, amt in totals:
        color = colors.get(cat, "white")
        console.print(f"[{color}]{cat:<10}[/{color}] : Rs. {amt:,.2f}")