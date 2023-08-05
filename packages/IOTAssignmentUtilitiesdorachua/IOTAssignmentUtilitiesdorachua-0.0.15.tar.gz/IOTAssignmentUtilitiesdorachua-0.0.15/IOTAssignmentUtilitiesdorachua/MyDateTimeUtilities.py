from datetime import datetime,timedelta

class MyDateTimeUtilities:

    def __init__(self):        
        self.datetime_created = datetime.now()

    def date_diff_in_seconds(self,dt2, dt1):
        timedelta = dt2 - dt1
        return timedelta.days * 24 * 3600 + timedelta.seconds