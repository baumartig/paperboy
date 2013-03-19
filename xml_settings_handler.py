import xml.sax, xml.sax.handler
from settings import Settings
import xml.etree.ElementTree as ET
import os.path

settingsPath = "data/settings.xml"

class SettingsHandler(xml.sax.handler.ContentHandler):

	def __init__(self):
		self.settings = Settings()
		self.buffer = ""
		self.attrBuffer = {}
		self.inMailSettings = False
		self.inSmtpServer = False

	def startElement(self, name, attributes):
		if name == "mail-settings": self.inMailSettings = True
		if name == "smtp-server": self.inSmtpServer = True

		for key in attributes.keys():
			self.attrBuffer.update({key: attributes[key]})

		return

	def characters(self, data):
		self.buffer += data

	def endElement(self, name):
		puffer = self.buffer.strip()

		if name == "calibre-folder":
			self.settings.setCalibreFolder(puffer)
		if name == "export-format":
			self.settings.setFormat(puffer)
		if self.inMailSettings:
			if name == "from":
				self.settings.setMailFrom(puffer)
			elif name == "to":
				self.settings.setMailTo(puffer)
				
			if self.inSmtpServer:
				if name == "address":
					self.settings.setSmtpServer(puffer,
						self.attrBuffer["port"],
						self.attrBuffer["security"])
				elif name == "login":
					self.settings.setSmtpLogin(puffer)
				elif name == "password":
					self.settings.setSmtpPassword(puffer)

		# reset the stuff
		if name == "mail-settings": self.inMailSettings = False
		elif name == "smtp-server": self.inSmtpServer = False
		self.buffer = ""
		self.attrBuffer = {}

def loadSettings():
	if os.path.isfile(settingsPath):
		parser = xml.sax.make_parser()
		handler = SettingsHandler()
		parser.setContentHandler(handler)
		parser.parse(settingsPath)
		return handler.settings
	else:
		return Settings()

def saveSettings(settings):
	root = ET.Element("configuration")
	tree = ET.ElementTree(root)

	appendTextElement(root, "calibre-folder", settings.calibreFolder)
	appendTextElement(root, "export-format", settings.format)

	mailElem = ET.SubElement(root, "mail-settings")
	appendTextElement(mailElem, "from", settings.mailFrom)
	appendTextElement(mailElem, "to", settings.mailTo)

	if settings.smtpServer:
		smtpElem = ET.SubElement(mailElem, "smtp-server")
		addressElem = appendTextElement(smtpElem, "address", settings.mailFrom)

		if "port" in settings.smtpServer:
			addressElem.set("port", str(settings.smtpServer["port"]))
		if "security" in settings.smtpServer:
			addressElem.set("security", settings.smtpServer["security"])
		if "login" in settings.smtpServer:
			appendTextElement(smtpElem, "login", settings.smtpServer["login"])
		if "password" in settings.smtpServer:
			appendTextElement(smtpElem, "password", settings.smtpServer["password"])

	tree.write(settingsPath)

	return

def appendTextElement(parent, tagName, text):
	newElem = ET.SubElement(parent, tagName)
	newElem.text = text
	return newElem