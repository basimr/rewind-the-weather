from django.shortcuts import render
from django.views import View

import requests

ACCUWEATHER_API_KEY = "WGXjPfYxPsbFYsZa9D2RBM00ScRIQVHb"
ACCUWEATHER_CITY_URL = "http://dataservice.accuweather.com/locations/v1/cities/search?apikey={}&q={}&language=en-us"
ACCUWEATHER_WEATHER_URL = "http://dataservice.accuweather.com/currentconditions/v1/{}?apikey={}&language=en-us"

OPENWEATHERMAP_API_KEY = "26c6d0e1cc1a1ae2acf09ad56c31fd22"
OPENWEATHERMAP_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"


class ApiException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return "Error {}".format(self.status_code)


class HomeView(View):

    @staticmethod
    def get(request):
        template = "index.html"
        context = {}
        return render(request, template, context)

    @staticmethod
    def post(request):
        city = request.POST.get("city", None)

        try:
            accuweather_data = get_accuweather(city)
            openweathermap_data = get_openweathermap(city)
        except ApiException as e:
            template = "error.html"
            context = {
                "status_code": e.status_code,
                "error_msg": "We probably couldn't find the city you requested. Sorry about that!"
            }
            return render(request, template, context)

        weather_datapoints = [
            accuweather_data,
            openweathermap_data,
        ]

        template = "weather.html"
        context = {
            "city": city,
            "datapoints": weather_datapoints,
        }

        return render(request, template, context)


def get_accuweather(city):
    city_url = ACCUWEATHER_CITY_URL.format(ACCUWEATHER_API_KEY, city)

    city_rsp = requests.get(city_url)
    city_data = city_rsp.json()[0]
    city_key = city_data["Key"]

    weather_url = ACCUWEATHER_WEATHER_URL.format(city_key, ACCUWEATHER_API_KEY)
    weather_rsp = requests.get(weather_url)
    if weather_rsp.status_code != 200:
        raise ApiException(weather_rsp.status_code)

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
    weather_rsp = requests.get(weather_url)
    if weather_rsp.status_code != 200:
        raise ApiException(weather_rsp.status_code)

    weather_data = weather_rsp.json()
    conditions = weather_data["weather"][0]["main"]
    temperature_k = weather_data["main"]["temp"]
    temperature_c = kelvin_to_celsius(temperature_k)

    return {
        "source": "OpenWeatherMap",
        "conditions": conditions,
        "temperature": int(temperature_c),
    }
