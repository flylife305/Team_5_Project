import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import sqlite3

############## Database setup
# Create a SQLite database to store user data
conn = sqlite3.connect("mortgage_data.db")
cursor = conn.cursor()


def fetch_data():
    cursor.execute("SELECT * FROM mortgage_data")
    rows = cursor.fetchall()
    for row in rows:
        print(row)  # or display in GUI widget

# === File to store user data ===
DATA_FILE = "users.json"

# === Load user data ===
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# === Save user data ===
def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

users = load_users()

# === AUTH WINDOW ===
def login_screen():
    auth_win = tk.Tk()
    auth_win.title("Login or Sign Up")

    tk.Label(auth_win, text="Username:", bg="lightblue").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(auth_win)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(auth_win, text="Password:", bg="lightblue").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(auth_win, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username in users and users[username]["password"] == password:
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            auth_win.destroy()
            open_calculator(username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def signup():
        username = username_entry.get()
        password = password_entry.get()
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
        elif not username or not password:
            messagebox.showerror("Error", "Fields cannot be empty.")
        else:
            users[username] = {
                "password": password,
                "mortgage_data": {}
            }
            save_users(users)
            messagebox.showinfo("Success", "Account created. You can now log in.")

    def logout():
        auth_win.destroy()

    tk.Button(auth_win, text="Login", command=login, bg="darkgreen").grid(row=2, column=0, pady=10)
    tk.Button(auth_win, text="Sign Up", command=signup, bg="darkgreen").grid(row=2, column=1)
    tk.Button(auth_win, text="Logout", command=logout, bg="darkgreen").grid(row=2, column=2)

    auth_win.configure(bg="lightblue")

    auth_win.mainloop()

# === CALCULATOR WINDOW ===
def open_calculator(username):
    user_data = users.get(username, {}).get("mortgage_data", {})

    print("Opening calculator window for user:", username)
    print("Current saved data:", user_data)

    root = tk.Tk()
    root.title("Mortgage Calculator")
    root.configure(bg="lightblue")

    # Price input field
    tk.Label(root, text="Price of Property($):", bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    price_entry = tk.Entry(root)
    price_entry.grid(row=0, column=1, padx=10, pady=5)
    price_entry.insert(0, user_data.get("price", ""))

    # Interest rate
    tk.Label(root, text="Interest Rate(%):", bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    interest_entry = tk.Entry(root)
    interest_entry.grid(row=1, column=1, padx=10, pady=5)
    interest_entry.insert(0, user_data.get("interest_rate", ""))

    # Down payment
    tk.Label(root, text="Down Payment($):", bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    down_payment_entry = tk.Entry(root)
    down_payment_entry.grid(row=2, column=1, padx=10, pady=5)
    down_payment_entry.insert(0, user_data.get("down_payment", ""))

    # Property tax
    tk.Label(root, text="Property Tax:", bg="lightblue").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    tax_entry = tk.Entry(root)
    tax_entry.grid(row=3, column=1, padx=10, pady=5)
    tax_entry.insert(0, user_data.get("property_tax", ""))

    # Loan term
    tk.Label(root, text="Loan Term (months):", bg="lightblue").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    term_entry = tk.Entry(root)
    term_entry.grid(row=4, column=1, padx=10, pady=5)
    term_entry.insert(0, user_data.get("loan_term", ""))

    tk.Label(root, text="Credit Score", bg="lightblue").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    credit_score_entry = tk.Entry(root)
    credit_score_entry.grid(row=5, column=1, padx=10, pady=5)
    credit_score_entry.insert(0, user_data.get("credit_score", ""))

    result_label = tk.Label(root, text="User Data", bg="lightblue")
    monthly_payment_label = tk.Label(root, text="Monthly Payment: $0.00", bg="lightblue")
    monthly_payment_label.grid(row=7, column=0, columnspan=2)

    result_label.grid(row=8, column=0, columnspan=2)

######## Function to classify credit score #######
    def classify_credit(credit_score):
        try:
            score = int(credit_score)
            if score <= 600:
                return "Minimally Qualified"
            elif 600 < score < 700:
                return "Moderately Qualified"
            else:
                return "Well Qualified"
        except:
            return "Unknown"
        
    def calculate_payment():
        try:
            price = float(price_entry.get())
            down_payment = float(down_payment_entry.get())
            interest_rate = float(interest_entry.get())
            term = int(term_entry.get())

            loan_amount = price - down_payment
            monthly_rate = interest_rate / 100 / 12
            n = term

            if monthly_rate == 0:
                monthly_payment = loan_amount / n
            else:
                monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)

            monthly_payment_label.config(text=f"Monthly Payment: ${monthly_payment:,.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric inputs.")
   
    # Function to save data

    def save_data():
        print("Saving data...")
        users[username]["mortgage_data"] = {
            "price": price_entry.get(),
            "interest_rate": interest_entry.get(),
            "down_payment": down_payment_entry.get(),
            "property_tax": tax_entry.get(),
            "loan_term": term_entry.get(),
            "credit_score": credit_score_entry.get()
            
        }
        save_users(users)
        messagebox.showinfo("Success", "Data saved successfully!")

        # Display the saved data below the inputs
        display_saved_data()

    # Function to display saved data below the input fields
    def display_saved_data():
        display_data = f"""
        Price: {users[username]["mortgage_data"].get("price", "")}
        Interest Rate: {users[username]["mortgage_data"].get("interest_rate", "")}
        Down Payment: {users[username]["mortgage_data"].get("down_payment", "")}
        Property Tax: {users[username]["mortgage_data"].get("property_tax", "")}
        Loan Term: {users[username]["mortgage_data"].get("loan_term", "")}
        Credit Score: {users[username]["mortgage_data"].get("credit_score", "")}
        """
        result_label.config(text=display_data)
        print("Displayed saved data:", display_data)

    # Show saved data when opening the window (if any data exists)
    display_saved_data()

    ####################### Navigation Buttons############
    tk.Button(root, text="Save Inputs", command=save_data, bg="darkgreen").grid(row=6, column=0, columnspan=2, pady=10)
    tk.Button(root, text="Calculate Payment", command=calculate_payment, bg="darkgreen").grid(row=7, column=1, columnspan=2, pady=10)
    tk.Button(root, text="Sign Out", command=login_screen, bg="darkgreen").grid(row=9, column=0, columnspan=2, pady=10)
    tk.Button(root, text="Exit App", command=root.quit, bg="darkgreen").grid(row=10, column=0, columnspan=2, pady=10)


    # Treeview for displaying DB data
    columns = ("Username", "Price", "Interest Rate", "Down Payment", "Property Tax", "Loan Term", "Credit Score")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    tree.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

    # Function to load JSON data into database and display in Treeview
    def load_json_to_db():
        try:
            with open("users.json", "r") as f:
                users_data = json.load(f)
            
            

            cursor.execute("DROP TABLE IF EXISTS mortgage_data")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS mortgage_data (
                username TEXT PRIMARY KEY,
                price TEXT,
                interest_rate TEXT,
                down_payment TEXT,
                property_tax TEXT,
                loan_term TEXT,
                credit_score TEXT
            )
            """)

            for username, user_info in users_data.items():
                mortgage = user_info.get("mortgage_data", {})
                if mortgage:
                    cursor.execute("""
                    INSERT OR REPLACE INTO mortgage_data (
                        username, price, interest_rate, down_payment, property_tax, loan_term, credit_score
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        username,
                        mortgage.get("price", ""),
                        mortgage.get("interest_rate", ""),
                        mortgage.get("down_payment", ""),
                        mortgage.get("property_tax", ""),
                        mortgage.get("loan_term", ""),
                        mortgage.get("credit_score", "")
                    ))

            conn.commit()
            messagebox.showinfo("Success", "Data loaded from users.json to database.")
            display_db_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    # Display the data from database in Treeview
    def display_db_data():
        for row in tree.get_children():
            tree.delete(row)

        cursor.execute("SELECT * FROM mortgage_data")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

    # Load data and display it when the button is clicked
    tk.Button(root, text="Update Table", command=lambda: [load_json_to_db(), display_db_data()], bg="darkgreen").grid(row=11, column=0, columnspan=2, pady=5)

    root.mainloop()
    conn.close()

# Start the app
login_screen()
