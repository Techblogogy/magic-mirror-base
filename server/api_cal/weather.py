import httplib2
import json

from api_cal.setup import setup

API_WEATHER_KEY = "ea1b2a690767c4cffc1832b89fe81d68"

class Weather:

    @staticmethod
    def w_current_temp():
        h = httplib2.Http()

        lt_ln = setup.get_position()

        (heads, resp) = h.request("http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&units=metric&appid=%s" % (lt_ln["lat"],lt_ln["lng"],API_WEATHER_KEY), "GET")
        resp = json.loads(resp)

        return int( round(int(resp['main']['temp'])) )
