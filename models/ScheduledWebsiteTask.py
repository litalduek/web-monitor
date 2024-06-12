class ScheduledWebsiteTask:
    def __init__(self, website, last_execution_time):
        self.website = website
        self.last_execution_time = last_execution_time
        self.next_execution_time = last_execution_time + self.website.interval

    def update_next_execution_time(self, current_time):
        self.last_execution_time = current_time
        self.next_execution_time = current_time + self.website.interval
