import httplib2
import json

# from api_cal.setup import setup

# import logging
# logger = logging.getLogger("TB")

# from tb_config import conf_file as g_cfg
# cfg = g_cfg().get_cfg()

# API_WEATHER_KEY = cfg.get("API KEYS", "weather_map")

class Weather:

    def __init__(self, setup, log, cfg):
        self.setup = setup
        self._log = log
        self._cfg = cfg

        self.api_weather_key = self._cfg.get("API KEYS", "weather_map")


    def w_current_temp(self):
        h = httplib2.Http()

        lt_ln = self.setup.get_position()

        (heads, resp) = h.request("http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&units=metric&appid=%s" % (lt_ln["lat"],lt_ln["lng"], self.api_weather_key), "GET")
        resp = json.loads(resp)

        return int( round(int(resp['main']['temp'])) )

    def w_temp_range(self):
        temp = self.w_current_temp()

        temp_min = int(temp/10) * 10
        temp_max = temp_min+10

        temp_dig = int(temp%10)

        if temp_dig <= 5:
            temp_max -= 5
        else:
            temp_min += 5

        return [temp, temp_min, temp_max]
