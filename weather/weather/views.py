from django.shortcuts import render
from django.views import View

import requests

ACCUWEATHER_API_KEY = "DPsbcTv1LENEppp4BBkNuMjnWyDESrTF"
ACCUWEATHER_CITY_URL = "http://dataservice.accuweather.com/locations/v1/cities/search?apikey={}&q={}&language=en-us"
ACCUWEATHER_WEATHER_URL = "http://dataservice.accuweather.com/currentconditions/v1/{}?apikey={}&language=en-us"

OPENWEATHERMAP_API_KEY = "26c6d0e1cc1a1ae2acf09ad56c31fd22"
OPENWEATHERMAP_WEATHER_URL = "https://openweathermap.org/data/2.5/weather?q={}&appid={}"


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
    city_url = ACCUWEATHER_CITY_URL.format(ACCUWEATHER_API_KEY, city)
    city_rsp = requests.get(city_url)
    city_data = city_rsp.json()[0]
    city_key = city_data["Key"]

    weather_url = ACCUWEATHER_WEATHER_URL.format(city_key, ACCUWEATHER_API_KEY)
    weather_rsp = requests.get(weather_url)
    weather_data = weather_rsp.json()[0]

    conditions = weather_data["WeatherText"]
    temperature = weather_data["Temperature"]["Metric"]["Value"]

    return {
        "source": "AccuWeather",
        "conditions": conditions,
        "temperature": int(temperature),
    }


def get_openweathermap(city):
    kelvin_to_celsius = lambda k: k - 273.15

    weather_url = OPENWEATHERMAP_WEATHER_URL.format(city, OPENWEATHERMAP_API_KEY)
    weather_url = "https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22"  # TODO change when my API key is active
    weather_rsp = requests.get(weather_url)
    weather_data = weather_rsp.json()

    conditions = weather_data["weather"][0]["main"]
    temperature_k = weather_data["main"]["temp"]
    temperature_c = kelvin_to_celsius(temperature_k)

    return {
        "source": "OpenWeatherMap",
        "conditions": conditions,
        "temperature": int(temperature_c),
    }
