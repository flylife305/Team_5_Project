import tkinter as tk
from tkinter import messagebox
import json
import os

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

    tk.Label(auth_win, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(auth_win)
    username_entry.grid(row=0, column=1)

    tk.Label(auth_win, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(auth_win, show="*")
    password_entry.grid(row=1, column=1)

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

    tk.Button(auth_win, text="Login", command=login).grid(row=2, column=0, pady=10)
    tk.Button(auth_win, text="Sign Up", command=signup).grid(row=2, column=1)

    auth_win.mainloop()

# === CALCULATOR WINDOW ===
def open_calculator(username):
    user_data = users.get(username, {}).get("mortgage_data", {})

    print("Opening calculator window for user:", username)
    print("Current saved data:", user_data)

    root = tk.Tk()
    root.title("Mortgage Calculator")
    root.geometry("500x500")

    tk.Label(root, text="Price of Property:").grid(row=0, column=0)
    price_entry = tk.Entry(root)
    price_entry.grid(row=0, column=1)
    price_entry.insert(0, user_data.get("price", ""))

    tk.Label(root, text="Interest Rate:").grid(row=1, column=0)
    interest_entry = tk.Entry(root)
    interest_entry.grid(row=1, column=1)
    interest_entry.insert(0, user_data.get("interest_rate", ""))

    tk.Label(root, text="Down Payment:").grid(row=2, column=0)
    down_payment_entry = tk.Entry(root)
    down_payment_entry.grid(row=2, column=1)
    down_payment_entry.insert(0, user_data.get("down_payment", ""))

    tk.Label(root, text="Property Tax:").grid(row=3, column=0)
    tax_entry = tk.Entry(root)
    tax_entry.grid(row=3, column=1)
    tax_entry.insert(0, user_data.get("property_tax", ""))

    tk.Label(root, text="Loan Term (months):").grid(row=4, column=0)
    term_entry = tk.Entry(root)
    term_entry.grid(row=4, column=1)
    term_entry.insert(0, user_data.get("loan_term", ""))

    result_label = tk.Label(root, text="")
    result_label.grid(row=6, column=0, columnspan=2)

    # Function to save data
    def save_data():
        print("Saving data...")
        users[username]["mortgage_data"] = {
            "price": price_entry.get(),
            "interest_rate": interest_entry.get(),
            "down_payment": down_payment_entry.get(),
            "property_tax": tax_entry.get(),
            "loan_term": term_entry.get()
        }
        save_users(users)
        messagebox.showinfo("Success", "Data saved successfully!")

        # Display the saved data below the inputs
        display_saved_data()

    # Function to display saved data below the input fields
    def display_saved_data():
        display_data = f"""
        Price: {users[username]['mortgage_data'].get('price', '')}
        Interest Rate: {users[username]['mortgage_data'].get('interest_rate', '')}
        Down Payment: {users[username]['mortgage_data'].get('down_payment', '')}
        Property Tax: {users[username]['mortgage_data'].get('property_tax', '')}
        Loan Term: {users[username]['mortgage_data'].get('loan_term', '')}
        """
        result_label.config(text=display_data)
        print("Displayed saved data:", display_data)

    # Show saved data when opening the window (if any data exists)
    display_saved_data()

    tk.Button(root, text="Save Inputs", command=save_data).grid(row=5, column=0, columnspan=2)
    def sign_out():
        root.destroy()  # Close the calculator window
        login_screen()  # Reopen the login screen

    # Add Close App button
    tk.Button(root, text="Sign Out", command=sign_out).grid(row=7, column=0, columnspan=2)

    root.mainloop()

# Start app
login_screen()