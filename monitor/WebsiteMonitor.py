import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
import yaml

import Config
from dao import MonitorDao
from models.ScheduledWebsiteTask import ScheduledWebsiteTask
from models.Website import Website
from utils import Logger


class WebsiteMonitor:
    def __init__(self):
        self.scheduled_website_task_list = None
        self.websites_list = None
        self.monitorDao = MonitorDao.MonitorDao()
        self.website_metrics_list = []
        self.logger = Logger.Logger().get_logger()
        self.stop_event = threading.Event()

        self.load_websites_data(Config.WEBSITES_DATA_YAML)
        self.setup_tasks()

    def load_websites_data(self, websites_data_yaml):
        try:
            self.websites_list = self._load_websites_from_yaml(websites_data_yaml)
        except FileNotFoundError:
            self.logger.error(f"YAML file not found: {websites_data_yaml}")
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML file: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error loading YAML file: {e}")

    def setup_tasks(self):
        self.scheduled_website_task_list = self._build_scheduled_website_task_list(self.websites_list)

    def monitor(self):
        self.logger.info("Start website monitoring...")
        threading.Thread(target=self._log_metrics, args=(Config.DB_BULK_SECONDS_INTERVAL,)).start()

        if self.scheduled_website_task_list:
            with ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
                while not self.stop_event.is_set():
                    current_time = time.time()
                    passed_time_tasks = list(
                        filter(lambda task: task.next_execution_time <= current_time, self.scheduled_website_task_list))
                    if not passed_time_tasks:
                        time.sleep(1)
                    else:
                        for scheduled_website_task in passed_time_tasks:
                            scheduled_website_task.update_next_execution_time(current_time)
                            executor.submit(self._check_website, scheduled_website_task.website)
            executor.shutdown(wait=True)

    def _check_website(self, website):
        try:
            checked_at = datetime.now()
            start_time = time.time()
            response = requests.get(website.url)
            response_time = time.time() - start_time
            status_code = response.status_code
            regex_matched = None

            if 200 <= status_code < 226:
                content = response.text
                regex_matched = bool(re.search(website.regex_pattern, content))

            website_metrics = (website.id, status_code, response_time, regex_matched, None, checked_at)
            self.logger.info(
                f"{checked_at} | Website ID: {website.id} | Status: {status_code} | Response Time: {response_time:.2f} sec | Regex Matched: {regex_matched}")
        except Exception as e:
            error_message = f"An unexpected error occurred while checking {website.url}: {str(e)}"
            website_metrics = (website.id, None, None, None, error_message, checked_at)
            self.logger.error(f"{checked_at} | Website ID: {website.id} {str(e)}")
        self.website_metrics_list.append(website_metrics)

    def _log_metrics(self, db_bulk_interval):
        while not self.stop_event.is_set():
            if self.website_metrics_list:
                self.monitorDao.insert_website_metrics(self.website_metrics_list)
            time.sleep(db_bulk_interval)

    def _load_websites_from_yaml(self, yaml_file):
        websites_list = []
        with open(yaml_file, 'r') as file:
            websites_data = yaml.safe_load(file)
        if websites_data:
            for website_data in websites_data['websites']:
                websites_list.append(Website(
                    website_data['url'],
                    website_data['interval'],
                    website_data['regex_pattern'])
                )

        return websites_list

    def _build_scheduled_website_task_list(self, websites_list):
        website_execution_tasks_list = []
        if websites_list:
            for website in websites_list:
                website_execution_task = ScheduledWebsiteTask(website, time.time())
                website_execution_tasks_list.append(website_execution_task)
        return website_execution_tasks_list

    def _stop(self):
        self.stop_event.set()
        self.logger.info("Website monitoring stopped.")
