class ScheduledWebsiteTask:
    def __init__(self, website, current_time):
        self.website = website
        self.next_execution_time = current_time + self.website.interval

    def update_next_execution_time(self, current_time):
        self.next_execution_time = current_time + self.website.interval
