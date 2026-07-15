import random
import smtplib
from email.message import EmailMessage
import sqlite3
from database import get_connection

# ==========================================
# CONFIGURATION - UPDATE THESE DETAILS
# ==========================================
SENDER_EMAIL = "prempayalpayal@gmail.com"  # The email that SENDS the OTP
SENDER_PASSWORD = "etfbpzpmwfbmhduu" # The 16-character App Password 

def send_otp_email(recipient_email):
    otp = str(random.randint(100000, 999999))
    
    msg = EmailMessage()
    msg['Subject'] = 'Your Expense Tracker Verification OTP'
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg.set_content(f'Hello,\n\nYour OTP for verifying your Expense Tracker registration is: {otp}\n\nDo not share this code with anyone.')

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return otp
    except Exception as e:
        print(f"\n[!] Error sending email: {e}")
        print("[!] Please check your email credentials and App Password.")
        return None

def sign_up():
    print("\n--- SIGN UP ---")
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    email = input("Enter your email address: ")

    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Check if username is already taken
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("\n[!] Username already exists. Please try a different one.")
        conn.close()
        return

    # 2. Send OTP to verify the new account
    print(f"\nSending verification OTP to {email}...")
    generated_otp = send_otp_email(email)
    
    if generated_otp:
        entered_otp = input("Enter the 6-digit OTP sent to your email: ")
        
        # 3. Only save to the database if the OTP matches perfectly
        if entered_otp == generated_otp:
            try:
                cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
                conn.commit()
                print("\n[+] Registration successful! You can now log in.")
            except sqlite3.IntegrityError:
                print("\n[!] Database error occurred during registration.")
        else:
            print("\n[!] Invalid OTP. Registration cancelled.")
    else:
        print("\n[!] Sign up failed because the verification email could not be sent.")
        
    conn.close()

def login():
    print("\n--- LOGIN ---")
    username = input("Username: ")
    password = input("Password: ")

    conn = get_connection()
    cursor = conn.cursor()
    
    # Instant check - no OTP screen during login anymore
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("\n[+] Login successful!")
        return user[0]  # Sends user straight to dashboard
    else:
        print("\n[!] Invalid username or password.")
        return None