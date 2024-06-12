import psycopg2

import Config

class DatabaseConnection:

    def __init__(self):
        self.conn = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(Config.DB_CONNECTION)
            return self.conn
        except psycopg2.OperationalError as e:
            self.logger.error(f"Error: Failed to establish a database connection. {e}")
        except Exception as e:
            self.logger.error(f"Error: An unexpected error occurred while connecting to the database. {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()



