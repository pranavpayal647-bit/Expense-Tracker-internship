import random
import smtplib
from email.message import EmailMessage
from rich.console import Console

console = Console()

# NOTE: Use an App Password if using Gmail (not your normal password)
SENDER_EMAIL = "personalexpensetracker9@gmail.com"      # <-- put your Gmail address here
SENDER_PASS = "yftd mmmk bmcm cwqx"        # <-- put your 16-char App Password here (no spaces or with spaces, both work)

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(receiver_email, otp):
    try:
        msg = EmailMessage()
        msg.set_content(f"Your PETS Registration OTP is: {otp}")
        msg['Subject'] = "PETS Registration Verification"
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email

        # SMTP configuration
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.send_message(msg)
        server.quit()
        console.print(f"[green]✅ OTP sent to {receiver_email}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]SMTP Error: {e}[/red]")
        console.print(f"[bold italic yellow]DEBUG FALLBACK - Your OTP is {otp}[/bold italic yellow]")
        return False  # don't silently succeed if email failed

def verify_otp_flow(email):
    otp = generate_otp()
    sent = send_otp_email(email, otp)

    if not sent:
        # Email failed — decide whether to still let them proceed using the console OTP
        console.print("[yellow]Email delivery failed, but you can still verify using the OTP printed above.[/yellow]")

    entered_otp = input("Enter the OTP sent to your email: ")
    return entered_otp == otp