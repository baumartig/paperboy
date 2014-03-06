from settings_handler import settings
from jobs_handler import jobs
from job import EXECUTION_TYPES as job_execution_types
from job import WEEKDAYS as job_weekdays
import recipes_handler
import jobs_handler
import os
import settings_handler
import jobs_executor
import util
import _Getch

def makeMenu(options, directInput=True):
	sortedKeys = sorted(options)
	for key in sortedKeys:
		print "%5s %s" % (key, options[key]["name"])

	if directInput:
		print "Selection: ",
		selection = _Getch.getch()
		print
	else:
		selection = raw_input("Selection (commit with Enter): ")
	while not selection in options:
		print "Invalid selection"
		if directInput:
			print "New selection: ",
			selection = _Getch.getch()
			print
		else:
			selection = raw_input("New Selection: ")


	if "arg" in options[selection]:
		options[selection]["function"](*options[selection]["arg"])
	else:
		options[selection]["function"]()

def mainMenu():
	clear()
	print "Welcome to the paperboy server"
	print "What would you like to do"

	makeMenu(mainOptions)

def jobsMenu():
	clear()
	print "Jobs Menu"
	makeMenu(jobsOptions)

def listJobs():
	clear()
	copyListJobOptions = listJobsOptions.copy()

	print "List jobs:"

	for (index, job) in enumerate(jobs, 1):
		copyListJobOptions[str(index)] = jobOption(job.recipeRef, index - 1)

	makeMenu(copyListJobOptions)

def jobProperties(job):
	clear()
	copyJobPropertiesOptions = jobPropertiesOptions.copy()

	index = jobs.index(job)
	
	copyJobPropertiesOptions["d"] = {"name":"delete job", "function":deleteJob, "arg":[index]}

	optionsList = []
	optionsList.append({"name":"execution type: %20s" % job.executionType, "function":changeJobInterval, "arg":[job]})
	optionsList.append({"name":"execution time: %20s" % util.formatTime(job.executionTime), "function":changeJobExecutionTime, "arg":[job]})
	if not job.executionType == "daily":
		optionsList.append({"name":"execution day : %20s" % job.executionDay, "function":changeJobExecutionDay, "arg":[job]})

	# append the options to the menu
	for (x, option)	in enumerate(optionsList, 1):
		copyJobPropertiesOptions[str(x)] = option

	print "Properties of \"%s\"" % job.recipeRef
	makeMenu(copyJobPropertiesOptions)


def changeJobInterval(job):
	intervalOptions = {}
	for (x, interval)	in enumerate(job_execution_types, 1):
		intervalOptions[str(x)] = {"name":interval, "function":setJobInterval, "arg":[job, job.setexecutiontype, interval]}
	intervalOptions["x"] = {"name":"exit menu", "function":jobProperties, "arg":[job]}

	makeMenu(intervalOptions)

def setJobInterval(job, function, interval):
	function(interval)
	jobs_handler.saveJobs(jobs)
	jobProperties(job)

def changeJobExecutionTime(job):
	new_time = None

	while not new_time:
		new_time_str = raw_input("New Execution Time: ")
		try :
			new_time = util.parseTime(new_time_str)
		except:
			new_time = None
			print "Invalid time formate please write HH:MM"

	job.setexecutiontime(new_time)
	jobs_handler.saveJobs(jobs)
	jobProperties(job)

def changeJobExecutionDay(job):
	if job.executionType == "weekly":
		dayOptions = {}
		for (x, day)	in enumerate(job_weekdays, 1):
			dayOptions[str(x)] = {"name":day, "function":setJobExecutionDay, "arg":[job, job.setexecutionday, day]}
		dayOptions["x"] = {"name":"exit menu", "function":jobProperties, "arg":[job]}		
		makeMenu(dayOptions)
	else:
		new_day = None
		while not new_day:
			new_day_str = raw_input("New execution day (1 to 30): ")
			try :
				new_day = int(new_day_str)
				if new_day < 1 or new_day > 30:
					new_day = None
					print "Invalid day please enter a number between 1 and 30."						
			except:
				new_day = None
				print "Invalid day please enter a number between 1 and 30."

		job.setexecutionday(new_day)
		jobs_handler.saveJobs(jobs)
		jobProperties(job)

def setJobExecutionDay(job, function, day):
	function(day)
	jobs_handler.saveJobs(jobs)
	jobProperties(job)


def jobOption(name, index):
	return {"name":"%s" %(name), "function":jobProperties, "arg": [jobs[index]]}

def deleteJob(index):
	jobs_handler.deleteJob(index)
	listJobs()

def newJob(startIndex=0):
	clear()
	nextIndex = startIndex + 10
	previousIndex = startIndex - 10
	recipes = recipes_handler.loadBuiltinRecipes()
	copyJobOptions = newJobOptions.copy()
	print "New Job (found %d)" % len(recipes)

	if startIndex > 0:
		copyJobOptions["p"]={"name":"previous 10 recipes", "function":newJob, "arg":[previousIndex]}
	if nextIndex < len(recipes):
		copyJobOptions["n"]={"name":"next 10 recipes", "function":newJob, "arg":[nextIndex]}
					

	for (recipe, x) in zip(recipes[startIndex:nextIndex], range(startIndex,nextIndex)):
		newJobOption(copyJobOptions, x, recipe)

	makeMenu(copyJobOptions, False)

def filterJobsTitle():
	newValue = raw_input("New Title Filter: ")
	recipes_handler.titleFilter = newValue
	newJob()

def filterJobsDescription():
	newValue = raw_input("New Description Filter: ")
	recipes_handler.descriptionFilter = newValue
	newJob()

def filterJobsLanguage():
	newValue = raw_input("New Language Filter: ")
	recipes_handler.languageFilter = newValue
	newJob()

def newJobOption(dict, x, recipe):
	dict[str(x + 1)] = {"name":"[%s]%s" %(recipe.language, recipe.title), "function":createJob, "arg":[recipe.title]}

def createJob(ref):
	newJob = jobs_handler.newJob(ref)
	jobProperties(newJob)

def exitToMainMenu():
	mainMenu()

def settingsMenu():
	clear()
	print "Settings:"
	copySettingsOptions = settingsOptions.copy()

	# colletct options
	optionsList = []
	optionsList.append(newOption("Builtin recipes folder", settings.calibreFolder, settings.setCalibreFolder))
	optionsList.append(newOption("Export format", settings.format, settings.setFormat))
	optionsList.append(newOption("Mail from", settings.mailFrom, settings.setMailFrom))
	optionsList.append(newOption("Mail To", settings.mailTo, settings.setMailTo))

	if settings.useSmtp():
		print "Using SMPT"
		copySettingsOptions["s"] = {"name":"Use sendmail", "function":sendmailSettings}
		optionsList.append(newOption("Smtp server", settings.smtpServer["address"], settings.setSmtpServerAdress))
		if "port" in settings.smtpServer:
			optionsList.append(newOption("Smtp port", settings.smtpServer["port"], settings.setSmtpServerPort))
		if "security" in settings.smtpServer:
			optionsList.append(newOption("Smtp security", settings.smtpServer["security"], settings.setSmtpServerSecurity))
		if "login" in settings.smtpServer:
			optionsList.append(newOption("Smtp login", settings.smtpServer["login"], settings.setSmtpLogin))
		if "password" in settings.smtpServer:
			encodedPw = "*"* len(settings.smtpServer["password"])
			optionsList.append(newOption("Smtp password", encodedPw, settings.setSmtpPassword))
	else:
		print "Using sendmail"
		copySettingsOptions["s"] = {"name":"Use smtp server", "function":createDefaultSmtpSettings}

	# append the options to the menu
	for (x, option)	in enumerate(optionsList, 1):
		copySettingsOptions[str(x)] = option

	print
	print "Options:"
	makeMenu(copySettingsOptions)

def quit():
	clear()
	print "Goodbye"

def editSetting(name, function):
	newValue = raw_input("%s: " % name)
	function(newValue)
	settings_handler.saveSettings()
	settingsMenu()

def createDefaultSmtpSettings():
	settings.setSmtpServer("localhost", 587, "starttls")
	settings.setSmtpLogin("username")
	settings.setSmtpPassword("username")
	settings_handler.saveSettings()
	settingsMenu()

def sendmailSettings():
	settings.deleteSmtpSettings()
	settings_handler.saveSettings()
	settingsMenu()

def newOption(name, option, function):
	return {"name":"%22s: %30s" %(name, str(option)), "function":editSetting, "arg": [name, function]}

def clear():
	os.system('clear')
	return

def executeJobs():
	clear()
	jobs_executor.execJobs(jobs)
	makeMenu(executeJobsOptions)

mainOptions = {	"1":{"name":"jobs", "function":jobsMenu},
				"2":{"name":"paperboy settings", "function":settingsMenu},
				"3":{"name":"execute jobs", "function":executeJobs},
				"q":{"name":"quit", "function":quit}}
jobsOptions = {	"1":{"name":"list jobs", "function":listJobs},
				"2":{"name":"new job", "function":newJob, "arg":[0]},
				"x":{"name":"exit menu", "function":exitToMainMenu}
				}

newJobOptions = {	"t":{"name":"filter title", "function":filterJobsTitle},
					# "d":{"name":"filter description", "function":filterJobsDescription},
					"l":{"name":"filter language", "function":filterJobsLanguage},
					"x":{"name":"exit menu", "function":jobsMenu}}

listJobsOptions = {"x":{"name":"exit menu", "function":jobsMenu}}

jobPropertiesOptions = {"x":{"name":"exit menu", "function":listJobs}}

executeJobsOptions = {"x":{"name":"goto main menu", "function":exitToMainMenu}}
settingsOptions = {"x":{"name":"exit menu", "function":exitToMainMenu}}

mainMenu()
