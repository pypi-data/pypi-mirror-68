from datetime import datetime


class Location:
    def __init__(self, latitude, longtitude, timestamp):
        self.latitude = latitude
        self.longtitude = longtitude
        self.timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") 

    def __str__(self):
        return str({'latitude': self.latitude, 'longtitude': self.longtitude, 'timestamp': self.timestamp})