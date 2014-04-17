import shelve
from job import Job

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


def test():
    print "Start test"
    global dbName
    dbName = "test.db"

    clear()
    jobs = loadJobs()
    assert len(jobs) == 0

    newJob = Job("test")
    addNewJob(newJob)
    jobs = loadJobs()
    assert len(jobs) == 1
    print jobs
    assert jobs.index(newJob) >= 0


if __name__ == "__main__":
    test()
