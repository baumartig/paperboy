# import xml_jobs_handler
import shelve_job_handler
from job import Job


def loadJobs():
    # return xml_jobs_handler.loadJobs()
    return shelve_job_handler.loadJobs()


def saveJobs(jobs):
    # xml_jobs_handler.saveJobs(jobs)
    shelve_job_handler.saveJobs(jobs)


def newJob(recipeRef):
    newJob = Job(recipeRef)
    shelve_job_handler.addNewJob(newJob)
    return newJob


def deleteJob(job):
    shelve_job_handler.deleteJob(job)


def doTest():
    print "Run Tests"
    # user other test db
    shelve_job_handler.dbName = "test.db"

    #create the first jobs
    job_1 = newJob("test_1")
    job_2 = newJob("test_2")
    jobs = [job_1, job_2]
    saveJobs(jobs)

    loadedJobs = loadJobs()
    for orgJob, loadedJob in zip(jobs, loadedJobs):
        if orgJob.recipeRef != loadedJob.recipeRef:
            print "Wrong job saved Original: %s vs. Saved: %s"\
                  % (orgJob.recipeRef, loadedJob.recipeRef)

    deleteJob(job_2)
    loadedJobs = loadJobs()

    if len(loadedJobs) >= len(jobs):
        print "Wrong size of loaded jobs after deleting one: %s" % loadedJobs

    # clear db and remove
    shelve_job_handler.clear()
    print "Tests finished"

if __name__ != "main":
    doTest()
