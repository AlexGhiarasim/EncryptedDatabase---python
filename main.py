import tkinter as tk
from tkinter import messagebox
from tkinter import font
from database.db_config import get_connection

def get_data():
    input_text = input_entry.get()
    output = f"Output: {input_text}"
    output_label.config(text=output)

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
    window.geometry("650x450")
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
