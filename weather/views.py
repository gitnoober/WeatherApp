from django.shortcuts import render , redirect
import requests
from .models import City
from .forms import CityForm
import config
# print(dir(config) , config.api_key)
# Create your views here.

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + config.api_key

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name'] # whatever they typed in the text box
            #check for duplicates
            city_cnt = City.objects.filter(name=new_city).count() #check the database

            if city_cnt == 0:
                res = requests.get(url.format(new_city)).json()
                if res['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Not a valid City!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    
    form = CityForm()
    cities = City.objects.all() # all the different cities whose weather we want to know

    weather_data = []

    for city in cities:

        res = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temp':res['main']['temp'],
            'description': res['weather'][0]['description'],
            'icon' : res['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    # print(data)
    
    context = {
        'weather_data':weather_data ,
        'form':form,
        'message':message,
        'message_class':message_class
    }


    return render(request , 'weather/weather.html', context)



def del_city(request , city_name):

    City.objects.get(name=city_name).delete()

    return redirect('home') 


def del_everycity(request):
    cities = City.objects.all()
    for city in cities:
        City.objects.get(name=city).delete()

    return redirect('home')