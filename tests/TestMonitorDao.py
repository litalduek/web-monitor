
import unittest

import psycopg2

import Config
from dao.MonitorDao import MonitorDao


class TestMonitorDao(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(Config.DB_CONNECTION)
        self.dao = MonitorDao()


    def tearDown(self):
        self.conn.close()

    def delete_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS website_metrics")
            self.conn.commit()

    def test_create_website_metrics_table(self):
        self.delete_table()
        # Ensure the table does not exist before creation
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name='website_metrics'")
            result = cursor.fetchone()
            self.assertIsNone(result)

        # Run the method to create the table
        self.dao.create_website_metrics_table()

        # Verify that the table has been created
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name='website_metrics'")
            result = cursor.fetchone()
            self.assertIsNotNone(result)

            # Verify the table schema
            cursor.execute(
                "SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='website_metrics'")
            columns = cursor.fetchall()

            expected_columns = [
                ('id', 'integer', 'NO'),
                ('website_id', 'integer', 'YES'),
                ('status_code', 'integer', 'YES'),
                ('response_time', 'double precision', 'YES'),
                ('checked_at', 'timestamp without time zone', 'YES'),
                ('regex_matched', 'boolean', 'YES'),
                ('error_message', 'text', 'YES')

            ]
            self.assertEqual(columns, expected_columns)


if __name__ == '__main__':
    unittest.main()