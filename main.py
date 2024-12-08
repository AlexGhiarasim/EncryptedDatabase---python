import tkinter as tk
from tkinter import messagebox
from tkinter import font
import random
import string
from database.db_config import get_connection
from file_operations.add_file import *
from file_operations.delete_file import *
from file_operations.read_file import *

def get_data():
    input_text = input_entry.get()
    try:
        parts = input_text.strip().split(" ", 1)
        if len(parts) != 2:
            raise ValueError("Invalid input! Use 'add file_path' or 'delete file_name' or 'read file_name'.")

        command, argument = parts

        if command.lower() == "add":
            encryption_key = "fe1a1915a379f3be5394b64d14794932"  # function to generate random key TODO
            encryption_method = "RSA"
            output = add_file(argument, encryption_key, encryption_method)

        elif command.lower() == "delete":
            output = delete_file(argument)

        elif command.lower() == "read":
            output = read_file(argument)

        else:
            raise ValueError("Invalid command. Accepted commands: add, delete, read.")

        output_label.config(text=output, fg="gray")

    except Exception as e:
        error_message = str(e)
        output_label.config(text=f"Error: {error_message}", fg="gray")
    
    input_entry.delete(0, tk.END)

def runApp():
    try:
        connection = get_connection()
        if connection:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if runApp():
    window = tk.Tk()
    window.title("Encrypted Security System")
    window.geometry("750x450")
    window.config(bg="#2e3b4e")

    title_font = font.Font(family="Helvetica", size=18, weight="bold")
    label_font = font.Font(family="Helvetica", size=12)
    output_font = font.Font(family="Helvetica", size=14, slant="italic")

    title_label = tk.Label(window, text="Encrypted Security System", font=title_font, fg="white", bg="#2e3b4e")
    title_label.pack(pady=20)

    input_label = tk.Label(window, text="Enter your input:", font=label_font, fg="white", bg="#2e3b4e")
    input_label.pack(pady=5)

    input_entry = tk.Entry(window, font=label_font, width=30, borderwidth=2, relief="solid")
    input_entry.pack(pady=10)

    fetch_button = tk.Button(window, text="Run", font=label_font, bg="#4CAF50", fg="white", width=20, height=2, command=get_data)
    fetch_button.pack(pady=15)

    output_label = tk.Label(window, text="Output will be displayed here!", font=output_font, fg="#F0F0F0", bg="#2e3b4e")
    output_label.pack(pady=10)

    close_button = tk.Button(window, text="Close", font=label_font, bg="#F44336", fg="white", width=20, height=2, command=window.quit)
    close_button.pack(pady=20)

    window.mainloop()
else:
    messagebox.showerror("Error", "The connection to the database could not be established!")
