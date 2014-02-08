import util

EXECUTION_TYPES = ["daily", "weekly", "monthly"]
WEEKDAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

class Job:

	def __init__(self, recipeRef):
		self.recipeRef = recipeRef.strip()
		self.executionType 	= "daily"
		self.executionTime	= util.parseTime("11:00")
		self.isExecuting	= False


	def setExecution(self, type, time, day=None):
		if type in EXECUTION_TYPES:
			self.executionType 	= type
			self.executionTime	= time
			self.executionDay = day
		else:
			raise JobException("Unknown execution type")

	def setExecutionType(self, type):
		if type in EXECUTION_TYPES:
			self.executionType 	= type
			if type == "weekly":
				self.executionDay = "Mo"
			if type == "monthly":
				self.executionDay = 1
		else:
			raise JobException("Unknown execution type")

	def setExecutionTime(self, time):
		self.executionTime	= time

	def setExecutionDay(self, day):
		self.executionDay = day

class JobException(Exception):

	def __init__(self, message):
		self.message = message
