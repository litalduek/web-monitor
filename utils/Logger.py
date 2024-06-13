import logging
import logging.config

class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger:
    _instance = None

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("WebWatchLogger")

    def get_logger(self):
        return self.logger

    # attribution: https://gist.github.com/Rustam-Z/aeb88b01b0f0d84e9f23240eeea2727f
