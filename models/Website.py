class Website:

    _MIN_INTERVAL_SECONDS = 5
    _MAX_INTERVAL_SECONDS = 300

    _id_counter = 1

    def __init__(self, url, interval, regex_pattern):
        self.id = Website._id_counter
        Website._id_counter += 1
        self.url = url
        self.interval = interval
        self.regex_pattern = regex_pattern
        self.validate_interval()

    def validate_interval(self):
        if self.interval < self._MIN_INTERVAL_SECONDS or self.interval > self._MAX_INTERVAL_SECONDS:
            raise ValueError(f"Interval must be between {self._MIN_INTERVAL_SECONDS} and {self._MAX_INTERVAL_SECONDS} seconds.")

    def __eq__(self, other):
        if isinstance(other, Website):
            return (self.id == other.id and
                    self.url == other.url and
                    self.interval == other.interval and
                    self.regex_pattern == other.regex_pattern)
        return False


