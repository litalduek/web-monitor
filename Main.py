import argparse
import signal

from dao.MonitorDao import MonitorDao
from monitor.WebsiteMonitor import WebsiteMonitor
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--create-table', action='store_true')
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if args.create_table:
        monitor_dao = MonitorDao()
        monitor_dao.create_website_metrics_table()
    else:
        global monitor
        monitor = WebsiteMonitor()
        monitor.monitor()

def signal_handler(signal, frame):
    if monitor:
        monitor._stop()

if __name__ == "__main__":
    main()









