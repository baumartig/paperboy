import builtin_recipes_handler

builtinRecipes = []
filteredRecipies = []

titleFilter = ""
descriptionFilter = ""
languageFilter = ""

def loadBuiltinRecipes():
	builtinRecipes = builtin_recipes_handler.loadBuiltinRecipes()
	return filterRecipes(builtinRecipes)

def filterByTitle(newTitleFilter):
	titleFilter = newTitleFilter
	filterRecipes()

def filterByDesc(newDescFilter):
	descriptionFilter = newDescFilter
	filterRecipes()

def filterByLang(newLangFilter):
	languageFilter = newLangFilter
	filterRecipes()

def filterRecipes(recipes):
	if (titleFilter
		or descriptionFilter
		or languageFilter):

		filteredRecipies = []
		for recipe in recipes:
			if (filter(recipe.title, titleFilter, filteredRecipies)
				and filter(recipe.description, descriptionFilter, filteredRecipies)
				and filter(recipe.language, languageFilter, filteredRecipies)):
				filteredRecipies.append(recipe)
	else:
		filteredRecipies = recipes[:]
	return filteredRecipies

def filter(value, filter, list):
	if filter:
		if value.find(filter) >= 0:
			return True
		else:
			return False
	else:
		return True