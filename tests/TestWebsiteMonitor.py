import os
import unittest
from unittest.mock import MagicMock, patch

import requests

from models.Website import Website
from monitor.WebsiteMonitor import WebsiteMonitor


class TestWebsiteMonitor(unittest.TestCase):
    def setUp(self):
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(project_dir)
        self.website_monitor = WebsiteMonitor()


    @patch('requests.get')
    def test_check_website_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Example content"
        mock_get.return_value = mock_response

        checked_website = Website("http://example.com", 20, "Example")
        self.website_monitor._check_website(checked_website)
        website_metrics_list = self.website_monitor.website_metrics_list
        website_metric = next((website for website in website_metrics_list if checked_website.id == website[0]), None)

        # Assert status_code
        self.assertEqual(website_metric[1], 200)
        # Assert response_time
        self.assertIsNotNone(website_metric[2])
        # Assert regex_matched
        self.assertTrue(website_metric[3])
        # Assert error_message
        self.assertIsNone(website_metric[4])
        # Assert checked_at
        self.assertIsNotNone(website_metric[5])



    @patch('requests.get')
    def test_check_website_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")

        checked_website = Website("http://example.com", 20, "Example")
        self.website_monitor._check_website(checked_website)
        website_metrics_list = self.website_monitor.website_metrics_list
        website_metric = next((website for website in website_metrics_list if checked_website.id == website[0]), None)

        # Assert status_code
        self.assertIsNone(website_metric[1])
        # Assert response_time
        self.assertIsNone(website_metric[2])
        # Assert regex_matched
        self.assertIsNone(website_metric[3])
        # Assert error_message
        self.assertEqual(website_metric[4], "An unexpected error occurred while checking http://example.com: Network error")
        # Assert checked_at
        self.assertIsNotNone(website_metric[5])
