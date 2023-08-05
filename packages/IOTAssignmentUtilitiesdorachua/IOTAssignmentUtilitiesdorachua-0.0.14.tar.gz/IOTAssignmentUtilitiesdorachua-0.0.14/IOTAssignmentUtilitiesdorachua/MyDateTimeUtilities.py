from datetime import datetime,timedelta

class MyDateTimeUtilities:

    def date_diff_in_seconds(self,dt2, dt1):
        timedelta = dt2 - dt1
        return timedelta.days * 24 * 3600 + timedelta.seconds