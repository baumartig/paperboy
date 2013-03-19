from settings_handler import settings
from jobs_handler import jobs
import recipes_handler
import jobs_handler
import os
import settings_handler
import jobs_executor

def makeMenu(options):
	sortedKeys = sorted(options)
	for key in sortedKeys:
		print "%5s %s" % (key, options[key]["name"])

	selection = raw_input("Selection: ")
	while not selection in options:
		print "Invalid selection"
		selection = raw_input("New selection: ")

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
	print "Input the job number to delete it."

	for (index, job) in enumerate(jobs):
		copyListJobOptions[str(index)] = jobOption(job.recipeRef, index)

	makeMenu(copyListJobOptions)

def jobOption(name, index):
	return {"name":"%s" %(name), "function":deleteJob, "arg": [index]}

def deleteJob(index):
	jobs_handler.deleteJob(index)
	listJobs()

def newJob(startIndex):
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

	makeMenu(copyJobOptions)

def filterJobsTitle():
	newValue = raw_input("New Title Filter: ")
	recipes_handler.titleFilter = newValue
	newJob(0)

def filterJobsDescription():
	newValue = raw_input("New Description Filter: ")
	recipes_handler.descriptionFilter = newValue
	newJob(0)

def filterJobsLanguage():
	newValue = raw_input("New Language Filter: ")
	recipes_handler.languageFilter = newValue
	newJob(0)

def newJobOption(dict, x, recipe):
	dict[str(x)] = {"name":"[%s]%s" %(recipe.language, recipe.title), "function":createJob, "arg":[recipe.title]}

def createJob(args):
	jobs_handler.newJob(0)
	listJobs()

def exitToMainMenu():
	mainMenu()

def settingsMenu():
	clear()
	print "Settings:"
	copySettingsOptions = settingsOptions.copy()

	# colletct options
	optionsList = []
	optionsList.append(newOption("Calibre folder", settings.calibreFolder, settings.setCalibreFolder))
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
	for (x, option)	in enumerate(optionsList):
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
	return {"name":"%20s: %30s" %(name, str(option)), "function":editSetting, "arg": [name, function]}

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
				"x":{"name":"exit menu", "function":exitToMainMenu}}

newJobOptions = {	"t":{"name":"filter title", "function":filterJobsTitle},
					# "d":{"name":"filter description", "function":filterJobsDescription},
					"l":{"name":"filter language", "function":filterJobsLanguage},
					"x":{"name":"exit menu", "function":jobsMenu}}

listJobsOptions = {"x":{"name":"exit menu", "function":jobsMenu}}

executeJobsOptions = {"x":{"name":"goto main menu", "function":exitToMainMenu}}
settingsOptions = {"x":{"name":"exit menu", "function":exitToMainMenu}}

mainMenu()