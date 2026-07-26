from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rich.console import Console
import database

console = Console()

def export_to_pdf(user_id, username):
    filename = f"{username}_report.pdf"
    expenses = database.get_all_expenses(user_id)
    
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, f"PETS Expense Report for {username}")
        
        c.setFont("Helvetica", 12)
        y = 700
        for exp in expenses:
            c.drawString(100, y, f"{exp[3]} | {exp[0]} ({exp[1]}) - Rs.{exp[2]}")
            y -= 20
            if y < 50:
                c.showPage()
                y = 750
        
        c.save()
        console.print(f"[bold green]✅ PDF Exported: {filename}[/bold green]")
    except Exception as e:
        console.print(f"[red]Error exporting PDF: {e}[/red]")