import tkinter as tk
from tkinter import messagebox
from tkinter import font
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
            output = add_file(argument, "RSA")

        elif command.lower() == "delete":
            output = delete_file(argument + ".enc")

        elif command.lower() == "read":
            output = read_file(argument + ".enc")

        else:
            raise ValueError("Invalid command. Accepted commands: add, delete, read.")

        output_label.config(text=output, fg="white")

    except Exception as e:
        error_message = str(e)
        output_label.config(text=f"Error: {error_message}", fg="red")

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

def on_enter(e, button, hover_color):
    button.config(bg=hover_color)

def on_leave(e, button, default_color):
    button.config(bg=default_color)

if runApp():
    window = tk.Tk()
    window.title("Encrypted Security System")
    window.geometry("800x500")
    window.config(bg="#1e293b")

    title_font = font.Font(family="Helvetica", size=24, weight="bold")
    label_font = font.Font(family="Helvetica", size=14)
    button_font = font.Font(family="Helvetica", size=12, weight="bold")
    output_font = font.Font(family="Helvetica", size=14, slant="italic")

    title_frame = tk.Frame(window, bg="#334155", pady=10)
    title_frame.pack(fill=tk.X)
    title_label = tk.Label(title_frame, text="Encrypted Security System", font=title_font, fg="white", bg="#334155")
    title_label.pack()

    spacer_frame = tk.Frame(window, bg="#1e293b", height=20)
    spacer_frame.pack()

    input_frame = tk.Frame(window, bg="#1e293b", pady=40)
    input_frame.pack()
    input_label = tk.Label(input_frame, text="Enter Command:", font=label_font, fg="white", bg="#1e293b")
    input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    input_entry = tk.Entry(input_frame, font=label_font, width=40, borderwidth=2, relief="solid")
    input_entry.grid(row=0, column=1, padx=10, pady=10)
    fetch_button = tk.Button(input_frame, text="Run Command", font=button_font, bg="#10b981", fg="white", command=get_data)
    fetch_button.grid(row=0, column=2, padx=10, pady=10)

    output_frame = tk.Frame(window, bg="#1e293b", pady=20)
    output_frame.pack(fill=tk.BOTH, expand=True)
    output_label = tk.Label(output_frame, text="Output will be displayed here!", font=output_font, fg="white", bg="#1e293b", wraplength=700, justify="left")
    output_label.pack(pady=10, padx=20)

    button_frame = tk.Frame(window, bg="#1e293b", pady=20)
    button_frame.pack()
    close_button = tk.Button(button_frame, text="Close Application", font=button_font, bg="#ef4444", fg="white", width=20, command=window.quit)
    close_button.pack(pady=10)

    fetch_button.bind("<Enter>", lambda e: on_enter(e, fetch_button, "#059669"))
    fetch_button.bind("<Leave>", lambda e: on_leave(e, fetch_button, "#10b981"))

    close_button.bind("<Enter>", lambda e: on_enter(e, close_button, "#dc2626"))
    close_button.bind("<Leave>", lambda e: on_leave(e, close_button, "#ef4444"))

    window.mainloop()
else:
    messagebox.showerror("Error", "The connection to the database could not be established!")
