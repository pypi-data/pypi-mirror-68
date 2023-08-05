from datetime import datetime
from .location import Location

class Track:
    def __init__(self, start_time, end_time):
        self.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
        self.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
        self.locations = []

    def add_location(self, location):
        self.locations.append(Location)

    def is_in_track(self, timestamp):
        return self.start_time <= timestamp <= self.end_time