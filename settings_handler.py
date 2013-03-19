import xml_settings_handler
from settings import Settings

def loadSettings():
	return xml_settings_handler.loadSettings()

def saveSettings():
	if settings:
		xml_settings_handler.saveSettings(settings)

settings = loadSettings()


