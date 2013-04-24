import subprocess
import os
import mail_handler
import tempfile
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

def execJob(job):
	job.isExecuting = True

	recipe = "\"%s\".recipe" % job.recipeRef
	output = tempfile.mkstemp(suffix="." + settings.format)	
	outputPath = output[1]

	try:
		returned = subprocess.call("ebook-convert %s %s" %(recipe,outputPath), shell=True)
		if returned != 0:
			print "Returned: " + returned
			job.isExecuting = False			
			return False

		# send the stuff
		subject = "%s %s" % (job.recipeRef, datetime.date(datetime.now()))
		mail_handler.sendMail(subject, "", outputPath)
	except Exception, e:
		pass

	# delete the tmp file
	os.remove(outputPath)
	job.isExecuting = False
	return True