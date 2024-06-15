import logging

import psycopg2

import Config


class DatabaseConnection:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.conn = self.connect(Config.DB_CONNECTION)

    def connect(self, db_connection):
        try:
            self.conn = psycopg2.connect(db_connection)
            return self.conn
        except psycopg2.OperationalError as e:
            self.logger.error(f"Error: Failed to establish a database connection. {e}")
        except Exception as e:
            self.logger.error(f"Error: An unexpected error occurred while connecting to the database. {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()

    def get_connection(self):
        return self.conn
