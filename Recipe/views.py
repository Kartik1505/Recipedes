from django.shortcuts import render,redirect
import requests
import json

#key: d819766523ae4583bc4bc4f8ac4deaab
#https://api.spoonacular.com/recipes/complexSearch?query=pasta
base_url = "https://api.spoonacular.com/recipes/"
apikey = "d819766523ae4583bc4bc4f8ac4deaab"

def home(request):
	randomRecipeApi = requests.get(base_url+"random?number=50&tags=vegetarian&apiKey="+apikey)
	randomRecipeApi = json.loads(randomRecipeApi.content)

	recipes = randomRecipeApi["recipes"]

	try:
		idList = []
		imageList = []
		titleList = []
		finalRandomRecipeList = []

		for i in range(len(recipes)):
			ids = randomRecipeApi["recipes"][i]["id"]
			image = randomRecipeApi["recipes"][i]["image"]
			title = randomRecipeApi["recipes"][i]["title"]


			idList.append(ids)
			imageList.append(image)
			titleList.append(title)

		for x in zip(idList,imageList,titleList):
			finalRandomRecipeList.append(x)

	
		context = {
			"finalRandomRecipeList":finalRandomRecipeList,
		}

	except:
		return redirect("home")
	return render(request, "home.html", context)


def dataRequest(request):
	global recipe_name_1
	recipe_name_1 = ""

	if request.method == "POST":
		recipe_name_1 =request.POST.get("recipe_1")

	api1 = requests.get(base_url+"complexSearch?query="+recipe_name_1+"&apiKey="+apikey)
	api = json.loads(api1.content)
	
	return api



def data(request):
	api = dataRequest(request)
	lists0 = []
	lists1 = []
	lists2 = []
	final_list = []

	results = api["results"]

	for i in range(len(results)):
		recpie_id = api["results"][i]["id"]
		name = api["results"][i]["title"]
		image=  api["results"][i]["image"]

		lists0.append(recpie_id)
		lists1.append(name)
		lists2.append(image)

	for x in zip(lists0,lists1,lists2):
		final_list.append(x)

	return final_list

def search(request):
	final_list = data(request)
	context= {
		"final_list":final_list,
	}
	return render(request, "recipe.html", context)


def recipe(request, id1):
	id1 = str(id1)
	none_variable = ""
	context = {}
	image = ""

	api1 = requests.get("https://api.spoonacular.com/recipes/"+id1+"/information?includeNutrition=false&apiKey="+apikey)
	api1 = json.loads(api1.content)

	ingImageList = []
	ingAmountList = [] 
	finalIngList = []

	ingInstructionList = []

	title = api1["title"]
	try:
		image = api1["image"]
	except:
		print("error")
	summary = api1["summary"]
	readyInMinutes = api1["readyInMinutes"]
	servings = api1["servings"]
	vegetarian = api1["vegetarian"]
	veryHealthy = api1["veryHealthy"]
	extendedIngredients = api1["extendedIngredients"]
	instruction = api1["analyzedInstructions"][0]["steps"]


	for i in range(len(extendedIngredients)):
		ingImage = api1["extendedIngredients"][i]["image"]
		ingamount = api1["extendedIngredients"][i]["originalString"]

		ingImageList.append(ingImage)
		ingAmountList.append(ingamount)


	for x in zip(ingImageList, ingAmountList):
		finalIngList.append(x)
		
	for m in range(len(instruction)):
		ingInstruction = api1["analyzedInstructions"][0]["steps"][m]["step"]

		ingInstructionList.append(ingInstruction)




	context = {
		"title":title,
		"image":image,
		"summary":summary,
		"readyInMinutes":readyInMinutes,
		"serving":servings,
		"veryHealthy":veryHealthy,
		"vegetarian":vegetarian,
		"finalIngList":finalIngList,
		"ingInstructionList":ingInstructionList,
		"none_variable":none_variable,
	}

	return render(request,"recipe_select.html", context)




