import xml.etree.ElementTree as ET

class Parser:

	def __init__(self, file_path):
		self.file_path = file_path

	def parse(self, file_path):
    	tree = ET.parse(file_path)
    	root = tree.getroot()
    	return root
    	# for child in root: printout(child)


	def printout(element):
    	print [element.tag, element.text, element.attrib]

#parse("data/configuration.xml")