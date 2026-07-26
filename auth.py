import random
import smtplib
from email.message import EmailMessage
from rich.console import Console

console = Console()

# NOTE: Use an App Password if using Gmail
SENDER_EMAIL = "prempayalpayal@gmail.com"
SENDER_PASS = "ccbsfdozwzwedyhl"

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
        return True
    except Exception as e:
        console.print(f"[yellow]SMTP Error: {e}. Falling back to DEBUG mode.[/yellow]")
        return True # For demonstration purposes if SMTP fails

def verify_otp_flow(email):
    otp = generate_otp()
    if send_otp_email(email, otp):
        console.print(f"[bold italic]DEBUG: Your OTP is {otp}[/bold italic]") 
        entered_otp = input("Enter the OTP sent to your email: ")
        return entered_otp == otp
    return False