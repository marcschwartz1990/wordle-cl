import sqlite3


class Database:
    def __init__(self, name):
        self.name = name
        self.conn = self.create_connection()
        self.cursor = self.create_cursor()

    def create_connection(self):
        """Creates a connection with the database and returns a connection object."""
        try:
            connection = sqlite3.connect(self.name)
            print(f"Connection to '{self.name}' successful")
        except Exception:
            print(f"Error: '{Exception}'")
        return connection

    def create_cursor(self):
        """Creates a cursor object."""
        try:
            cursor = self.conn.cursor()
            print(f"Cursor created successfully")
        except Exception:
            print(f"Error: '{Exception}'")
        return cursor

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print('Query successful')
        except Exception:
            print(f"Error: '{Exception}'")

    def close(self):
        self.conn.close()
