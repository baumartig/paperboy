import xml_jobs_handler
from job import Job


def loadJobs():
	return xml_jobs_handler.loadJobs()

def saveJobs(jobs):
	xml_jobs_handler.saveJobs(jobs)

def newJob(recipeRef):
	newJob = Job(recipeRef)
	jobs.append(newJob)
	saveJobs(jobs)

def deleteJob(index):
	jobs.pop(index)
	saveJobs(jobs)

jobs = loadJobs()