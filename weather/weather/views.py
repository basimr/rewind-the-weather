from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

import requests

API_KEY = "DPsbcTv1LENEppp4BBkNuMjnWyDESrTF"

ACCUWEATHER_CITY_DATA = "http://dataservice.accuweather.com/locations/v1/cities/search?apikey={}&q={}&language=en-us"
ACCUWEATHER_WEATHER_DATA = "http://dataservice.accuweather.com/currentconditions/v1/{}?apikey={}&language=en-us"


class HomeView(View):

    @staticmethod
    def get(request):
        template = "index.html"
        context = {}
        return render(request, template, context)


    @staticmethod
    def post(request):
        city = request.POST.get('city', None)

        weather_data = [
            get_accuweather(city),
            get_openweathermap(city),
        ]

        template = "weather.html"
        context = {
            "weather_data": weather_data,
        }

        return render(request, template, context)


def get_accuweather(city):
    city_url = ACCUWEATHER_CITY_DATA.format(API_KEY, city)
    city_rsp = requests.get(city_url)
    city_data = city_rsp.json()[0]
    city_key = city_data["Key"]

    weather_url = ACCUWEATHER_WEATHER_DATA.format(city_key, API_KEY)
    weather_rsp = requests.get(weather_url)
    weather_data = weather_rsp.json()[0]

    conditions = weather_data["WeatherText"]
    temperature = weather_data["Temperature"]["Metric"]["Value"]

    return {
        "source": "AccuWeather",
        "conditions": conditions,
        "temperature": temperature,
    }


def get_openweathermap(city):
    pass