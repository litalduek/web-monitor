import argparse
import logging
import signal

from dao.MonitorDao import MonitorDao
from monitor.WebsiteMonitor import WebsiteMonitor


class Application:
    def __init__(self):
        self.monitor = None

    def signal_handler(self, signal, frame):
        if self.monitor:
            self.monitor.stop()

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--create-table', action='store_true')
        args = parser.parse_args()

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        if args.create_table:
            MonitorDao().create_website_metrics_table()
        else:
            self.monitor = WebsiteMonitor()
            self.monitor.monitor()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )


if __name__ == "__main__":
    setup_logging()
    app = Application()
    app.run()
