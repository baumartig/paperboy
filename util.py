from datetime import datetime

TIME_FORMAT = "%H:%M"

def parseTime(time_str):
	return datetime.strptime(time_str, TIME_FORMAT)

def formatTime(time):
	return datetime.strftime(time, TIME_FORMAT)