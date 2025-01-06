import os
from database.db_config import get_connection
from encryption.encryption_operations import decrypt_file
import tempfile
import sys
sys.setrecursionlimit(1000000)

def read_file(file_name):
    """
    This function reads a file from the disk and decrypts it.

    Parameters:
    file_name (str): The name of the file that needs to be read.

    Returns:
    str: A message indicating the result of the operation.
    """
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
        decrypt_file(file_path, private_key) 
    else:
        with open(file_path, "rb") as file:
            content = file.read()

    return f"File read and saved successfully!"