import logging

import psycopg2

from connection.DatabaseConnection import DatabaseConnection


class MonitorDao:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_connection = DatabaseConnection().get_connection()

    def create_website_metrics_table(self):
        try:
            self.db_connection.cursor().execute('''
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
            self.db_connection.commit()
            self.logger.info("Table 'website_metrics' created successfully.")
        except psycopg2.ProgrammingError as e:
            self.logger.error(f"Error: Failed to create the website_metrics table. {e}")
        except Exception as e:
            self.logger.error(f"Error: An unexpected error occurred while creating the website_metrics table.{e}")

    def insert_website_metrics(self, website_metrics_list):
        self.db_connection.cursor().executemany('''
            INSERT INTO website_metrics (website_id, status_code, response_time, regex_matched, error_message, checked_at)
            VALUES (%s, %s,%s, %s,%s, %s)''', website_metrics_list)
        self.db_connection.commit()
