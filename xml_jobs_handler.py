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
		return

	def characters(self, data):
		self.buffer += data

	def endElement(self, name):
		if name == "job":
			# build job
			job = Job(self.recipeRef)
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
		jobElem = ET.SubElement(root, "job")

		recipeRefElem = ET.SubElement(jobElem, "recipeRef")
		recipeRefElem.text = job.recipeRef

	tree.write(jobsPath)

	return