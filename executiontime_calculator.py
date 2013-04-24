from datetime import datetime
from datetime import timedelta
from job import WEEKDAYS
from job import Job
from jobs_handler import jobs

def calculateNextExecution(job):
	now = datetime.now()
	executionTime = datetime.now()

	if job.executionType == "weekly":
		diff = WEEKDAYS.index(job.executionDay) - now.weekday()
		executionTime = executionTime.replace(day= now.day + diff)
		

	elif job.executionType == "monthly":
		executionTime = executionTime.replace(day = int(job.executionDay))

	# add the calculated difference
	executionTime = executionTime.replace(hour=job.executionTime.hour,
							minute=job.executionTime.minute)

	
	addition = timedelta()
	if now > executionTime:
		#add intervall
		if job.executionType == "daily":
			addition = timedelta(days=1)
		if job.executionType == "weekly":
			addition = timedelta(weeks=1)
		elif job.executionType == "monthly":
			if executionTime.month < 12:
				executionTime = executionTime.replace(month=executionTime.month + 1)
			else:
				executionTime = executionTime.replace(month=1)
	# add the delta
	executionTime = executionTime + addition

	# set the next execution date on the job
	job.nextExecution = executionTime

def test():
	# testDaily()
	# testWeekly()
	testMonthly()
	return

def testMonthly():
	job = Job("testRef")
	now = datetime.now()

	# execute later
	addition = timedelta(hours=1)
	job.setExecution("monthly", (now + addition).time(), now.day)

	calculateNextExecution(job)
	print "Current time: " + str(now)
	print "Next execution: " + str(job.nextExecution)

	# execute tomorrow
	addition = timedelta(hours=-1)
	job.setExecution("monthly", (now + addition).time(), now.day)

	calculateNextExecution(job)
	print "Current time: " + str(now)
	print "Next execution: " + str(job.nextExecution)

def testWeekly():
	job = Job("testRef")
	now = datetime.now()

	# execute later
	addition = timedelta(hours=1)
	job.setExecution("weekly", (now + addition).time(), "So")

	calculateNextExecution(job)
	print "Current time: " + str(now)
	print "Next execution: " + str(job.nextExecution)

	# execute tomorrow
	addition = timedelta(hours=-1)
	job.setExecution("weekly", (now + addition).time(), "So")

	calculateNextExecution(job)
	print "Current time: " + str(now)
	print "Next execution: " + str(job.nextExecution)

def testDaily():
	job = Job("testRef")
	now = datetime.now()

	# execute later
	addition = timedelta(hours=1)
	job.setExecution("daily", (now + addition).time())

	calculateNextExecution(job)
	print "Current time: " + str(now)
	print "Next execution: " + str(job.nextExecution)

	# execute tomorrow
	addition = timedelta(hours=-1)
	job.setExecution("daily", (now + addition).time())

	calculateNextExecution(job)
	print "Current time: " + str(now)
	print "Next execution: " + str(job.nextExecution)
	


test()
