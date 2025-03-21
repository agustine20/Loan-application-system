import sqlite3
import random

# Database setup
conn = sqlite3.connect("loan_system.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    age INTEGER,
    income REAL,
    employment_years INTEGER,
    credit_score INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    interest_rate REAL,
    duration INTEGER,
    status TEXT DEFAULT 'Pending',
    remaining_balance REAL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)''')

conn.commit()

# Function to register a user
def register_user():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    age = int(input("Enter your age: "))
    income = float(input("Enter your monthly income: "))
    employment_years = int(input("Enter years of employment: "))
    credit_score = random.randint(300, 850)  # Simulated credit score

    if age < 18:
        print("You must be 18 or older to register.")
        return

    try:
        cursor.execute("INSERT INTO users (name, email, age, income, employment_years, credit_score) VALUES (?, ?, ?, ?, ?, ?)", 
                       (name, email, age, income, employment_years, credit_score))
        conn.commit()
        print(f"User registered successfully! Your credit score is {credit_score}.")
    except sqlite3.IntegrityError:
        print("Email already exists. Try logging in.")

# Function to check loan eligibility
def check_eligibility(user):
    age, income, employment_years, credit_score = user[2], user[3], user[4], user[5]

    if age < 18:
        print("You must be at least 18 to apply for a loan.")
        return False
    if income < 20000:  # Example: Minimum monthly income
        print("Your income is too low to qualify for a loan.")
        return False
    if employment_years < 1:
        print("You must be employed for at least 1 year to qualify.")
        return False
    if credit_score < 600:
        print("Your credit score is too low to qualify for a loan.")
        return False

    return True

# Function to apply for a loan
def apply_loan(user_email):
    cursor.execute("SELECT * FROM users WHERE email=?", (user_email,))
    user = cursor.fetchone()
    
    if not user:
        print("User not found! Register first.")
        return

    if not check_eligibility(user):
        print("Loan application denied due to eligibility factors.")
        return

    amount = float(input("Enter loan amount: "))
    interest_rate = float(input("Enter interest rate (e.g., 5 for 5%): ")) / 100
    duration = int(input("Enter duration (months): "))

    total_payable = amount * (1 + interest_rate)
    cursor.execute("INSERT INTO loans (user_id, amount, interest_rate, duration, remaining_balance) VALUES (?, ?, ?, ?, ?)",
                   (user[0], amount, interest_rate * 100, duration, total_payable))
    conn.commit()
    print("Loan application submitted. Awaiting approval.")

# Function to view loans
def view_loans(user_email):
    cursor.execute("SELECT id FROM users WHERE email=?", (user_email,))
    user = cursor.fetchone()
    
    if not user:
        print("User not found!")
        return

    cursor.execute("SELECT * FROM loans WHERE user_id=?", (user[0],))
    loans = cursor.fetchall()

    if loans:
        print("Your Loans:")
        for loan in loans:
            print(f"Loan ID: {loan[0]}, Amount: {loan[2]}, Interest Rate: {loan[3]}%, Duration: {loan[4]} months, Status: {loan[5]}, Balance: {loan[6]}")
    else:
        print("No loans found.")

# Function to approve loans (Admin)
def approve_loan():
    loan_id = int(input("Enter Loan ID to approve: "))
    cursor.execute("UPDATE loans SET status='Approved' WHERE id=?", (loan_id,))
    conn.commit()
    print("Loan approved successfully!")

# Main Menu
def main():
    while True:
        print("\nLoan Management System")
        print("1. Register")
        print("2. Apply for Loan")
        print("3. View Loans")
        print("4. Approve Loan (Admin)")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            email = input("Enter your email: ")
            apply_loan(email)
        elif choice == "3":
            email = input("Enter your email: ")
            view_loans(email)
        elif choice == "4":
            approve_loan()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()