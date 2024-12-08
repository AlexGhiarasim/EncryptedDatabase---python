import os
import shutil
from database.db_config import get_connection

BASE_DIR = "./encrypted_files"

def add_file(file_path, encryption_key, encryption_method):
    if os.path.exists(file_path):  # exists local
        final_path = file_path  
    else:
        absolute_path = os.path.abspath(file_path)
        if os.path.exists(absolute_path): # exists absolute -> for example: C:\\...\\file.txt
            final_path = absolute_path 
        else:
            return "File to add not found!"

    if not os.path.exists(BASE_DIR): # create directory to store files
        os.makedirs(BASE_DIR)

    file_name = os.path.basename(final_path)
    stored_file_path = os.path.join(BASE_DIR, file_name)

    shutil.copy(final_path, stored_file_path) # copy file to encrypted_files directory

    query = """
    INSERT INTO file_metadata (file_name, file_path, encryption_key, encryption_method) VALUES (%s, %s, %s, %s) RETURNING id;
"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (file_name, stored_file_path, encryption_key, encryption_method))
            file_id = cur.fetchone()[0]
            conn.commit()

    return "File added on database and encrypted successfully!"
