from django.contrib import messages
import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def sample(request):
    msg="welcome"
    return HttpResponse(msg)

def index(request):

    data=None
    name=None
    calories=None
    fat=None
    sugar=None
    protein=None
    cholestrol=None
    carbohydrate=None
    fiber=None
    exercise=None

    if request.method=="GET" and 'query' in request.GET:
        query = request.GET.get('query') # get the user input from the form
        api_url = 'https://api.calorieninjas.com/v1/nutrition?query='

        # make API request
        response = requests.get(api_url + query, headers={'X-Api-Key': '6KnHuwZSjerfRrTZkjjnrQ==ou8W5uRcumXQo33i'})

        if response.status_code == 200:
            data=response.json() # get the data as json
            try:
                name = data['items'][0]['name']
                calories = data['items'][0]['calories']
                fat = data['items'][0]['fat_total_g']
                sugar = data['items'][0]['sugar_g']
                protein = data['items'][0]['protein_g']
                cholestrol = data['items'][0]['cholesterol_mg']
                carbohydrate = data['items'][0]['carbohydrates_total_g']
                fiber = data['items'][0]['fiber_g']

                if calories > 100 and calories < 200:
                    exercise = {"walking": 38, "yoga": 44, "weightlifting": 48, "bicycling": 44}
                elif calories > 200 and calories < 300:
                    exercise = {"walking": 35, "yoga": 35, "weightlifting": 22, "bicycling": 19}
                elif calories > 300 and calories < 400:
                    exercise = {"walking": 16, "yoga": "18-27", "weightlifting": 21, "bicycling": 17}
                elif calories > 400 and calories < 500:
                    exercise = {"walking": 21, "yoga": 17, "weightlifting": "21-35", "bicycling": "21-35"}
                elif calories > 500 and calories < 600:
                    exercise = {"walking": 12, "yoga": 17, "weightlifting": 17, "bicycling": 17}
                elif calories > 600:
                    exercise = {"walking": 9, "yoga": "9-12", "weightlifting": "10-15", "bicycling": "13-18"}
                else:
                    messages.error(request,"You don't have any excercise to burn your calories!")

            except IndexError:
                messages.error(request, "No data found for your search !")


    return render(request,r"MyAppHTML/index.html",context={
        'name':name,
        'calories':calories,
        'fat':fat,
        'sugar':sugar,
        'protein':protein,
        'cholestrol':cholestrol,
        'carbohydrate':carbohydrate,
        'fiber':fiber,
        'exercise':exercise
    })