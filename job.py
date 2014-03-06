import util

EXECUTION_TYPES = ["daily", "weekly", "monthly"]
WEEKDAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


class Job:

    def __init__(self, recipe_ref):
        self.recipe_ref = recipe_ref.strip()
        self.execution_type = "daily"
        self.execution_time = util.parseTime("11:00")
        self.is_executing = False
        self.execution_day = None
        self.next_execution = None

    def setexecution(self, execution_type, time, day=None):
        if execution_type in EXECUTION_TYPES:
            self.execution_type = execution_type
            self.execution_time = time
            if execution_type == "weekly":
                if day in WEEKDAYS:
                    self.execution_day = day
                else:
                    raise JobException("Unknown Weekday " + day + " only these are allowed: " + WEEKDAYS)
            elif execution_type == "monthly":
                self.execution_day = int(day)
        else:
            raise JobException("Unknown execution type")

    def setexecutiontype(self, execution_type):
        if execution_type in EXECUTION_TYPES:
            self.execution_type = execution_type
            if execution_type == "weekly":
                self.execution_day = "Mo"
            if execution_type == "monthly":
                self.execution_day = 1
        else:
            raise JobException("Unknown execution type")

    def setexecutiontime(self, time):
        self.execution_time = time

    def setexecutionday(self, day):
        self.execution_day = day


class JobException(Exception):

    def __init__(self, message):
        self.message = message
