import os
import shutil
from database.db_config import get_connection
from encryption.encryption_operations import *

BASE_DIR = "./encrypted_files"

def add_file(file_path, encryption_method):
    """
    Add a file to the database, encrypt it, and store the private key.
    """
    if os.path.exists(file_path):  # Check if the file exists locally
        final_path = file_path  
    else:
        absolute_path = os.path.abspath(file_path)
        if os.path.exists(absolute_path):  # Check if the file exists with an absolute path
            final_path = absolute_path 
        else:
            return "File to add not found!"  # Return if the file doesn't exist

    if not os.path.exists(BASE_DIR): 
        os.makedirs(BASE_DIR)

    public_key, private_key = generate_keys()

    encrypted_file_path = encrypt_and_save_file(final_path, public_key)

    file_name = os.path.basename(final_path) + '.enc'
    stored_file_path = os.path.join(BASE_DIR, file_name)

    query = """
    INSERT INTO file_metadata (file_name, encryption_key, encryption_method, file_path) 
    VALUES (%s, %s, %s, %s) RETURNING id;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (file_name, private_key, encryption_method, stored_file_path))
            conn.commit()

    return "File added to database, encrypted, and private key saved successfully!"

def encrypt_and_save_file(file_path, public_key):
    """
    Encrypt the file and save it in the encrypted_files directory.
    """
    encrypted_file_path = file_path + '.enc'

    encrypt_file(file_path, public_key)

    file_name = os.path.basename(file_path) + '.enc'
    encrypted_file_path = os.path.join(BASE_DIR, file_name)
    
    shutil.move(file_path + '.enc', encrypted_file_path)

