from datetime import datetime
from datetime import timedelta
from job import WEEKDAYS
from job import Job


def calculateNextExecution(job, now=datetime.now()):
    executionTime = now.replace()

    if job.executionType == "weekly":
        diff = WEEKDAYS.index(job.executionDay) - now.weekday()
        if diff < 0 and now.day < (-1 * diff):
            diff += now.day
            executionTime.replace(month=executionTime.month - 1)

        executionTime = executionTime.replace(day=now.day + diff)

    elif job.executionType == "monthly":
        executionTime = executionTime.replace(day=job.executionDay)

    # add the calculated difference
    executionTime = executionTime.replace(hour=job.executionTime.hour,
                                            minute=job.executionTime.minute,
                                            second=job.executionTime.second,
                                            microsecond=job.executionTime.microsecond)

    addition = timedelta()
    if now > executionTime:
        #add interval
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
    test_monthly()
    test_weekly()
    testDaily()
    return


def test_monthly():
    print "TEST Monthly"
    job = Job("testRef")
    now = datetime(2014, 2, 2, 10)

    # execute later
    addition = timedelta(hours=1)
    job.setExecution("monthly", (now + addition).time(), now.day)

    calculateNextExecution(job, now)
    assert datetime(2014, 2, 2, 11) == job.nextExecution,     "Calculated wrong execution date: %s"\
                                                               % str(job.nextExecution)

    # execute tomorrow
    addition = timedelta(hours=-1)
    job.setExecution("monthly", (now + addition).time(), now.day)

    calculateNextExecution(job, now)
    assert datetime(2014, 3, 2, 9) == job.nextExecution,      "Calculated wrong execution date: %s"\
                                                               % str(job.nextExecution)
    print "OK"


def test_weekly():
    print "TEST Weekly"
    job = Job("testRef")
    now = datetime(2014, 2, 2, 10)

    # execute later
    addition = timedelta(hours=1)
    job.setExecution("weekly", (now + addition).time(), "So")

    calculateNextExecution(job, now)
    assert datetime(2014, 2, 2, 11) == job.nextExecution, "Calculated wrong execution date: %s"\
                                                           % str(job.nextExecution)

    # execute tomorrow
    addition = timedelta(hours=-1)
    job.setExecution("weekly", (now + addition).time(), "So")

    calculateNextExecution(job, now)
    assert datetime(2014, 2, 9, 9) == job.nextExecution,  "Calculated wrong execution date: %s"\
                                                           % str(job.nextExecution)
    print "OK"


def testDaily():
    print "TEST Daily"
    job = Job("testRef")
    now = datetime(2014, 2, 2, 10)

    # execute later
    addition = timedelta(hours=1)
    job.setExecution("daily", (now + addition).time())

    calculateNextExecution(job, now)
    assert datetime(2014, 2, 2, 11) == job.nextExecution, "Calculated wrong execution date: %s"\
                                                           % str(job.nextExecution)

    # execute tomorrow
    addition = timedelta(hours=-1)
    job.setExecution("daily", (now + addition).time())

    calculateNextExecution(job, now)
    assert datetime(2014, 2, 3, 9) == job.nextExecution, "Calculated wrong execution date: %s"\
                                                          % str(job.nextExecution)
    print "OK"

if __name__ == '__main__':
	test()
