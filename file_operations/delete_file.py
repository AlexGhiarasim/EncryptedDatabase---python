from database.db_config import get_connection
import os

def delete_file(file_name):
    """
    This function deletes a file from the database first and then attempts to delete it from the disk.

    Parameters:
    file_name (str): The name of the file that needs to be deleted.

    Returns:
    str: A message indicating the result of the operation.
    """
    query = "SELECT id, file_path FROM file_metadata WHERE file_name = %s;"
    delete_query = "DELETE FROM file_metadata WHERE file_name = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (file_name,))
            result = cur.fetchone()

            if not result:
                return f"File {file_name} not found in database!"

            _, file_path = result

            cur.execute(delete_query, (file_name,))
            conn.commit()

            if os.path.exists(file_path):
                os.remove(file_path)

    return f"File {file_name} deleted successfully from the database!"
