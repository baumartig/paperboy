import jobs_handler
import time
import jobs_executor
from datetime import datetime
from datetime import time as Time

excTime = Time(23, 00)

def printJobs(jobs):
	for job in jobs:
		print "\t Job: %s" % job.recipeRef


jobs = jobs_handler.loadJobs()
print "Welcome to the paperboy server"


print "Job execution time: %s" % excTime

jobsLen = len(jobs)
if jobsLen == 0:
	print "Currently we have no job to run"
elif jobsLen == 1:
	print "Currently we have one job to run:"
else:
	print "Currently we have %d jobs to run:" % jobsLen

printJobs(jobs)

while True:
	currentTime = datetime.time(datetime.now())
	if excTime.hour == currentTime.hour and excTime.minute == currentTime.minute:
		if jobs_executor.execJobs(jobs):
			time.sleep(60)
		else:
			print "Error in the execution"
			break
	time.sleep(30)