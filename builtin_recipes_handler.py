import xml.sax, xml.sax.handler
from settings_handler import settings
from recipe import Recipe

class RecipesHandler(xml.sax.handler.ContentHandler):

    def __init__(self):
        self.recipes = []

    def startElement(self, name, attributes):
        if name == "recipe":
            title = attributes["title"]
            description = attributes["description"]
            language = attributes["language"]

            newRecipe = Recipe(title, description, language)
            self.recipes.append(newRecipe)



def loadBuiltinRecipes():
    parser = xml.sax.make_parser()
    handler = RecipesHandler()
    parser.setContentHandler(handler)
    parser.parse(settings.calibreFolder + "/builtin_recipes.xml")
    return handler.recipes