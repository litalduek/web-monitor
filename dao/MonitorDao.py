import psycopg2

from connection import DatabaseConnection
from utils import Logger


class MonitorDao:

    def __init__(self):
        self.logger = Logger.Logger().get_logger()

    def create_website_metrics_table(self):
        try:
            with DatabaseConnection.DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('''
                     CREATE TABLE IF NOT EXISTS website_metrics (
                         id SERIAL PRIMARY KEY,
                         website_id INTEGER,
                         status_code INTEGER,
                         response_time FLOAT,
                         checked_at TIMESTAMP,
                         regex_matched BOOLEAN,
                         error_message TEXT
                     )
                 ''')
                    conn.commit()
            self.logger.info("Table 'website_metrics' created successfully.")
        except psycopg2.ProgrammingError as e:
            self.logger.error(f"Error: Failed to create the website_metrics table. {e}")
        except Exception as e:
            self.logger.error(f"Error: An unexpected error occurred while creating the website_metrics table.{e}")

    def insert_website_metrics(self, website_metrics_list):
        with DatabaseConnection.DatabaseConnection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany('''
                       INSERT INTO website_metrics (website_id, status_code, response_time, regex_matched, error_message, checked_at)
                       VALUES (%s, %s,%s, %s,%s, %s)''', website_metrics_list)
                conn.commit()
