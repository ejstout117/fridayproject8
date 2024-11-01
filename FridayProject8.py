import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
def create_database():
    conn = sqlite3.connect("customer_feedback.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            feedback TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to submit feedback
def submit_feedback():
    name = entry_name.get()
    email = entry_email.get()
    feedback = text_feedback.get("1.0", tk.END).strip()
    
    if not name or not email or not feedback:
        messagebox.showerror("Error", "All fields must be filled out.")
        return
    
    conn = sqlite3.connect("customer_feedback.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (name, email, feedback) VALUES (?, ?, ?)", (name, email, feedback))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Feedback submitted successfully!")
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    text_feedback.delete("1.0", tk.END)

# Function to retrieve feedback with password protection
def retrieve_feedback():
    password = input("Enter password to view feedback: ")
    
    # Hardcoded password for simplicity; in practice, store securely
    if password != "securepassword":
        print("Access denied. Incorrect password.")
        return
    
    conn = sqlite3.connect("customer_feedback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    feedback_entries = cursor.fetchall()
    conn.close()
    
    if feedback_entries:
        print("Customer Feedback Entries:")
        for entry in feedback_entries:
            print(f"ID: {entry[0]}, Name: {entry[1]}, Email: {entry[2]}, Feedback: {entry[3]}")
    else:
        print("No feedback entries found.")

# GUI setup
root = tk.Tk()
root.title("Customer Feedback Application")
root.geometry("400x300")

# Input fields for name, email, and feedback
tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root, width=40)
entry_email.pack()

tk.Label(root, text="Feedback").pack()
text_feedback = tk.Text(root, width=40, height=5)
text_feedback.pack()

# Submit button
submit_button = tk.Button(root, text="Submit Feedback", command=submit_feedback)
submit_button.pack()

# Retrieve data button
retrieve_button = tk.Button(root, text="Retrieve Feedback (Console)", command=retrieve_feedback)
retrieve_button.pack()

# Initialize database and run the GUI
create_database()
root.mainloop()
