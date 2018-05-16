
# this probably isn't a necessary as a class but I'm going to build it out anyway
# might be useful in the future to have this as a class rather than a function
class Schedule(object):
    def __init__(self, raw_schedule):
        self.minutes = self.generate_minutes_list(raw_schedule)

    def generate_minutes_list(self, raw_schedule):
        minutes = {}
        i = 0
        for hour in list(range(0, 24)):
            for minute in list(range(0, 60)):
                minutes[i] = hour in raw_schedule['hour_starts'] and minute < raw_schedule['duration_mins']
                i += 1

        return minutes
