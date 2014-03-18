import shelve

dbName = "data/jobs.shelve"

def loadJobs():
	db = shelve.open(dbName)
	jobs = list(db.values())
	db.close()
	return jobs

def saveJobs(jobs):
	db = shelve.open(dbName)
	for job in jobs:
		db[str(job.id)] = job
	db.close()


def addNewJob(job):
	db = shelve.open(dbName)
	id = len(db)
	job.id = id 
	db[str(id)] = job
	db.close()

def deleteJob(job):
	db = shelve.open(dbName)
	db.pop(str(job.id))
	db.close()

def clear():
	db = shelve.open(dbName)
	db.clear()
	db.close()