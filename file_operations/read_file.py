import os
from database.db_config import get_connection
from encryption.encryption_operations import decrypt_file 
import tempfile
import tkinter as tk
import sys
sys.setrecursionlimit(1000000)

def read_file(file_name):
    query = "SELECT file_path, encryption_key FROM file_metadata WHERE file_name = %s;"
    update_last_accessed = "UPDATE file_metadata SET last_accessed = CURRENT_TIMESTAMP WHERE file_name = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (file_name,))
            result = cur.fetchone()

            if not result:
                return f"File {file_name} not found in database!"

            if len(result) != 2:
                return f"Unexpected result format: {result}"
            
            file_path = result[0]
            private_key = result[1]

            cur.execute(update_last_accessed, (file_name,))
            conn.commit()

    if not os.path.exists(file_path):
        return f"File {file_path} not found on disk!"

    if file_path.endswith('.enc'):
        content = decrypt_file(file_path, private_key) 
    else:
        with open(file_path, "rb") as file:
            content = file.read()
    print(content)
    show_content_in_window(content)
    return f"File read successfully!"

def show_content_in_window(content):
    if content is None:
        print("Error: No content to display.")
        return

    window = tk.Tk()
    window.title("File content")

    window.geometry("600x400")
    window.resizable(False, False)

    text_widget = tk.Text(window)
    text_widget.pack(fill=tk.BOTH, expand=True)

    if isinstance(content, bytes):
        try:
            text_widget.insert(tk.END, content.decode('utf-8'))
        except UnicodeDecodeError:
            print("Error: Cannot decode in UTF-8 format.")
    elif isinstance(content, str):
        text_widget.insert(tk.END, content)
    else:
        print("Error: Unknown!")

    close_button = tk.Button(window, text="Close", command=window.quit)
    close_button.pack()

    window.mainloop()

def open_temp_file(content):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        if isinstance(content, str):
            content = content.encode('utf-8')
        temp_file.write(content)
        temp_file_path = temp_file.name
        os.startfile(temp_file_path)
