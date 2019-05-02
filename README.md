# Rewind the Weather

Don't you wish you could rewind the weather to one week ago, when it was brighter and sunnier?

Unfortunately that's impossible (for now)... But how about an application that lets you shop around for the best weather? This application allows you to view weather data from AccuWeather and OpenWeatherMap, letting you pick the weather you enjoy better!

## Installation

Follow these instructions inside a bash shell, which should work whether you're running Linux, macOs, or something like Cygwin on Windows.

1. `git clone https://github.com/basimr/rewind-the-weather.git`
2. `cd rewind-the-weather`
3. `virtualenv -p $(which python3) env`
4. `source env/bin/activate`
5. `pip install django requests`
6. `cd weather`
7. `python manage.py runserver`
8. Open http://localhost:8000/ in your web browser
9. Enjoy your weather shopping!
