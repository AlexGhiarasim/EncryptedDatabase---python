import os
import shutil
from database.db_config import get_connection
from encryption.encryption_operations import *

BASE_DIR = "./encrypted_files"

def add_file(file_path, encryption_method):
    """
    This function performs several checks regarding the existence of the file and the BASE_DIR directory, 
    and then generates a key pair (public and private) for my file, which are used for encrypting the file and 
    saving it to disk. Finally, the data is stored in the database after the encryption operation is successful.

    Parameters:
    file_path (str): The path to the file that needs to be encrypted.
    encryption_method (str): The method used for encryption. -> RSA

    Returns:
    str: A message indicating the result of the operation.
    
    """
    if os.path.exists(file_path):
        final_path = file_path  
    else:
        absolute_path = os.path.abspath(file_path)
        if os.path.exists(absolute_path):
            final_path = absolute_path 
        else:
            return "File to add not found!"

    if not os.path.exists(BASE_DIR): 
        os.makedirs(BASE_DIR)

    file_name = os.path.basename(final_path) + '.enc'

    query_check = "SELECT id FROM file_metadata WHERE file_name = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query_check, (file_name,))
            existing_entry = cur.fetchone()
            if existing_entry:
                return f"A file with the name '{file_name}' already exists in the database."

    public_key, private_key = generate_key_pair()
    encrypt_and_save_file(final_path, public_key)

    stored_file_path = os.path.join(BASE_DIR, file_name)

    query_insert = """
    INSERT INTO file_metadata (file_name, encryption_key, encryption_method, file_path) 
    VALUES (%s, %s, %s, %s) RETURNING id;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query_insert, (file_name, private_key, encryption_method, stored_file_path))
            conn.commit()

    return "File encrypted successfully! Private key stored in database!"

def encrypt_and_save_file(file_path, public_key):
    """
    This function encrypts the file using the public key and saves it to the BASE_DIR directory.

    Parameters:
    file_path (str): The path to the file that needs to be encrypted.
    public_key (str): The public key used for encryption.

    Returns:
    str: The final path where the encrypted file is saved.
    """
    encrypted_file_path = encrypt_file(file_path, public_key)
    
    final_encrypted_file_path = os.path.join(BASE_DIR, os.path.basename(encrypted_file_path))

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    shutil.move(encrypted_file_path, final_encrypted_file_path)
    print(f"File encrypted and moved to: {final_encrypted_file_path}")

    os.remove(file_path)
    print(f"Original file {file_path} has been deleted.")

    return final_encrypted_file_path
