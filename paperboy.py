import jobs_handler
import time
import jobs_executor
import executiontime_calculator
from datetime import datetime


def printJobs(jobs):
    for job in jobs:
        print "\t Job: %s" % job.recipeRef


jobs = jobs_handler.loadJobs()
print "Welcome to the paperboy server"


jobsLen = len(jobs)
if jobsLen == 0:
    print "Currently we have no job to run"
elif jobsLen == 1:
    print "Currently we have one job to run:"
else:
    print "Currently we have %d jobs to run:" % jobsLen

print "Calculating execution times:"
for job in jobs:
    executiontime_calculator.calculateNextExecution(job)
    print "%s : %s" % (job.recipeRef, job.nextExecution)

while True:
    now = datetime.now()
    for job in jobs:
        if job.nextExecution <= now and not job.isExecuting:
            print "job excecution time %s" % (job.nextExecution)
            if jobs_executor.execJob(job):
                time.sleep(60)
                executiontime_calculator.calculateNextExecution(job)
                print "new job excecution time %s" % (job.nextExecution)
            else:
                print "Error in the execution"
    time.sleep(30)
