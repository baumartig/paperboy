from datetime import datetime
from datetime import timedelta
from job import WEEKDAYS
from job import Job


def calculate_next_execution(job, now=datetime.now()):
    execution_time = now.replace()

    if job.execution_type == "weekly":
        diff = WEEKDAYS.index(job.execution_day) - now.weekday()
        if diff < 0 and now.day < (-1 * diff):
            diff += now.day
            execution_time.replace(month=execution_time.month - 1)

        execution_time = execution_time.replace(day=now.day + diff)

    elif job.execution_type == "monthly":
        execution_time = execution_time.replace(day=job.execution_day)

    # add the calculated difference
    execution_time = execution_time.replace(hour=job.execution_time.hour,
                                            minute=job.execution_time.minute,
                                            second=job.execution_time.second,
                                            microsecond=job.execution_time.microsecond)

    addition = timedelta()
    if now > execution_time:
        #add interval
        if job.execution_type == "daily":
            addition = timedelta(days=1)
        if job.execution_type == "weekly":
            addition = timedelta(weeks=1)
        elif job.execution_type == "monthly":
            if execution_time.month < 12:
                execution_time = execution_time.replace(month=execution_time.month + 1)
            else:
                execution_time = execution_time.replace(month=1)
    # add the delta
    execution_time = execution_time + addition

    # set the next execution date on the job
    job.next_execution = execution_time


def test():
    test_monthly()
    test_weekly()
    test_daily()
    return


def test_monthly():
    print "TEST Monthly"
    job = Job("testRef")
    now = datetime(2014, 2, 2, 10)

    # execute later
    addition = timedelta(hours=1)
    job.setexecution("monthly", (now + addition).time(), now.day)

    calculate_next_execution(job, now)
    assert datetime(2014, 2, 2, 11) == job.next_execution,     "Calculated wrong execution date: %s"\
                                                               % str(job.next_execution)

    # execute tomorrow
    addition = timedelta(hours=-1)
    job.setexecution("monthly", (now + addition).time(), now.day)

    calculate_next_execution(job, now)
    assert datetime(2014, 3, 2, 9) == job.next_execution,      "Calculated wrong execution date: %s"\
                                                               % str(job.next_execution)
    print "OK"


def test_weekly():
    print "TEST Weekly"
    job = Job("testRef")
    now = datetime(2014, 2, 2, 10)

    # execute later
    addition = timedelta(hours=1)
    job.setexecution("weekly", (now + addition).time(), "So")

    calculate_next_execution(job, now)
    assert datetime(2014, 2, 2, 11) == job.next_execution, "Calculated wrong execution date: %s"\
                                                           % str(job.next_execution)

    # execute tomorrow
    addition = timedelta(hours=-1)
    job.setexecution("weekly", (now + addition).time(), "So")

    calculate_next_execution(job, now)
    assert datetime(2014, 2, 9, 9) == job.next_execution,  "Calculated wrong execution date: %s"\
                                                           % str(job.next_execution)
    print "OK"


def test_daily():
    print "TEST Daily"
    job = Job("testRef")
    now = datetime(2014, 2, 2, 10)

    # execute later
    addition = timedelta(hours=1)
    job.setexecution("daily", (now + addition).time())

    calculate_next_execution(job, now)
    assert datetime(2014, 2, 2, 11) == job.next_execution, "Calculated wrong execution date: %s"\
                                                           % str(job.next_execution)

    # execute tomorrow
    addition = timedelta(hours=-1)
    job.setexecution("daily", (now + addition).time())

    calculate_next_execution(job, now)
    assert datetime(2014, 2, 3, 9) == job.next_execution, "Calculated wrong execution date: %s"\
                                                          % str(job.next_execution)
    print "OK"


test()
