import xml.sax, xml.sax.handler
import xml.etree.ElementTree as ET
from job import Job
import os.path

jobsPath = "data/jobs.xml"

class JobsHandler(xml.sax.handler.ContentHandler):

	def __init__(self):
		self.jobs = []
		self.buffer = ""

	def startElement(self, name, attributes):
		self.attributes = attributes
		return

	def characters(self, data):
		self.buffer += data

	def endElement(self, name):
		if name == "job":
			# build job
			job = Job(self.recipeRef)
			executionType 	= self.attributes["type"]
			executionTime	= self.attributes["time"]
			if (not executionType == "daily"):
				executionDay = self.attributes["day"]

			job.setExecution(executionType, executionTime, executionDay)
			self.jobs.append(job)

		if name == "recipeRef":
			self.recipeRef = self.buffer

		self.buffer = ""

def loadJobs():
	if os.path.isfile(jobsPath):
		parser = xml.sax.make_parser()
		handler = JobsHandler()
		parser.setContentHandler(handler)
		parser.parse(jobsPath)
		return handler.jobs
	else:
		return []

def saveJobs(jobs):
	root = ET.Element("jobs")
	tree = ET.ElementTree(root)

	for job in jobs:
		attributes = {}
		attributes["type"] = job.executionType
		attributes["time"] = job.executionTime
		if (not job.executionType == "daily"):
			attributes["day"] = job.executionDay

		jobElem = ET.SubElement(root, "job", attributes)

		recipeRefElem = ET.SubElement(jobElem, "recipeRef")
		recipeRefElem.text = job.recipeRef

	tree.write(jobsPath)

	return