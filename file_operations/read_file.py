import os
from database.db_config import get_connection
import tempfile
import tkinter as tk

def read_file(file_name):
    query = "SELECT id, file_path FROM file_metadata WHERE file_name = %s;"
    update_last_accessed = "UPDATE file_metadata SET last_accessed = CURRENT_TIMESTAMP WHERE file_name = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (file_name,))
            result = cur.fetchone()
            if not result:
                return f"File {file_name} not found in database!"
            _ , file_path = result

            cur.execute(update_last_accessed, (file_name,))
            conn.commit()

    if not os.path.exists(file_path):
       return f"File {file_path} not found on disk!"

    with open(file_path, "rb") as file:
        content = file.read()

    show_content_in_window(content)

def show_content_in_window(content):
    window = tk.Tk()
    window.title("File content")

    window.geometry("600x400")
    window.resizable(False, False)

    text_widget = tk.Text(window)
    text_widget.pack(fill=tk.BOTH, expand=True)

    text_widget.insert(tk.END, content.decode('utf-8'))

    close_button = tk.Button(window, text="Close", command=window.quit)
    close_button.pack()

    window.mainloop()

def open_temp_file(content):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name
        os.startfile(temp_file_path)

