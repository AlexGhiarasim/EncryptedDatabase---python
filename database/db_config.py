import psycopg2

db_config = {
    "dbname": "EncryptedSecuritySystem",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5432,
}

class DatabaseConnection:
    def __init__(self, db_config):
        self.db_config = db_config
        self._connection = None
    
    def try_connection(self):
        if self._connection is None:
            try:
                self._connection = psycopg2.connect(**self.db_config)
                print("Connected successfully to the database!")
            except Exception as e:
                print(f"Error at connection to the database: {e}")
                raise e
        
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()
            print("Connection closed!")
        else:
            print("No connection to close!")

db_connection = DatabaseConnection(db_config)

def get_connection():
    return db_connection.try_connection()
