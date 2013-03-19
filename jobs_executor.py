import subprocess
import os
import mail_handler
from datetime import datetime
from settings_handler import settings

def execJobs(jobs):
	try:
		for job in jobs:
			if not execJob(job):
				return False
		print "Jobs executed"
		return True
	except:
		print "Executed failed"
		return False
	finally:
		output = "tmp/output.mobi"
		if os.path.isfile(output):
			os.remove(output)

def execJob(job):
	recipe = "\"%s\".recipe" % job.recipeRef
	output = "tmp/output.%s" % settings.format

	returned = subprocess.call("ebook-convert %s %s" %(recipe,output) ,shell=True)
	if returned != 0:
		print "Returned: " + returned
		return False

	# send the stuff
	subject = "%s %s" % (job.recipeRef, datetime.date(datetime.now()))
	mail_handler.sendMail(subject, "", output)

	# delete the tmp file
	os.remove(output)
	return True