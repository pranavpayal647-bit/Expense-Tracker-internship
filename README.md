💰 PETS — Personal Expense Tracker System

A command-line personal expense tracker built in Python. PETS lets you register with email OTP verification, log expenses, set monthly budgets, search your spending history, view visual analytics, and export reports to CSV or PDF — all from a clean terminal dashboard powered by Rich.

✨ Features
🔐 Secure Registration — Email-based OTP verification before account creation
💵 Expense Tracking — Add expenses with item description, category, and amount
📊 Budget Management — Set a monthly budget and get warned when you exceed it
📈 Visual Analytics — Budget progress bar and category-wise spending breakdown
🔎 Advanced Search — Search expenses by keyword across item name or category
📄 Export Reports — Export your expense history to CSV or PDF
🗑️ Clear History — Wipe all expense records with confirmation
🖥️ Rich Terminal UI — Colorful tables, panels, and progress bars in the console
🛠️ Tech Stack
Component	Technology
Language	Python 3
Database	SQLite (sqlite3)
Terminal UI	Rich
PDF Export	ReportLab
Email/OTP	smtplib, email.message
📁 Project Structure
Expense-Tracker-internship/
├── main.py           # Entry point — handles login/register flow & dashboard
├── auth.py           # OTP generation & email verification logic
├── database.py       # SQLite connection, schema, and CRUD operations
├── analytics.py       # Budget meter & category breakdown visualizations
├── search.py          # Keyword-based expense search
├── csv_exporter.py    # Export expenses to CSV
├── pdf_export.py      # Export expenses to PDF
└── expenses.db         # SQLite database (auto-created on first run)
🚀 Getting Started
Prerequisites
Python 3.9+
A Gmail account with an App Password enabled (for sending OTP emails)
Installation
Clone the repository:
bash
   git clone https://github.com/<your-username>/Expense-Tracker-internship.git
   cd Expense-Tracker-internship
Install dependencies:
bash
   pip install rich reportlab
Configure email credentials in auth.py:
python
   SENDER_EMAIL = "your_email@gmail.com"
   SENDER_PASS = "your_16_char_app_password"

⚠️ You must use a Gmail App Password, not your regular account password. Enable it via: Google Account → Security → 2-Step Verification → App Passwords.

Run the application:
bash
   python main.py
📖 Usage

On launch, you'll be prompted to either register a new account or log in:

--- PERSONAL EXPENSE TRACKER SYSTEM (PETS) ---
1. Register New Account
2. Login to Dashboard

Registering sends a 6-digit OTP to your email for verification before account creation.

Once logged in, the dashboard offers:

1. Add Expense
2. Set Monthly Budget
3. View Expenses & Current Overview
4. Advanced Search
5. View Visual Analytics
6. Export CSV
7. Export PDF
8. Clear Expense History
9. Logout

Type back at any input prompt to cancel and return to the menu.

🧾 Sample Exports
CSV — <username>_report.csv with columns: Item, Category, Amount, Date
PDF — <username>_report.pdf with a formatted expense report
🔒 Security Notes
Passwords are currently stored in plaintext in the database — this is intended for learning/demo purposes only and should not be used in production without hashing (e.g. bcrypt).
Do not commit real email credentials — consider using environment variables instead of hardcoding SENDER_EMAIL / SENDER_PASS.
🗺️ Roadmap / Possible Improvements
 Hash passwords before storing
 Move credentials to environment variables / .env file
 Add expense editing/deletion (not just full clear)
 Add date-range filtering for search and reports
 Add multi-currency support
📄 License

This project is open source and available for educational use.
