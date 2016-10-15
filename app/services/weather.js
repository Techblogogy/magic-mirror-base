
app.factory("weather", ["$http", function ($http) {

    var appid = "ea1b2a690767c4cffc1832b89fe81d68";

    var getParams = function (lat, lng) {
        return {
            "lat": lat,
            "lon": lng,
            "units": "metric",
            "appid": appid,
        }
    };

    return {
        getWeather: function (lat, lng) {
            return $http.get("http://api.openweathermap.org/data/2.5/weather", {
                params: getParams(lat, lng)
            });
        },

        getForecast: function (lat, lng) {
            return $http.get("http://api.openweathermap.org/data/2.5/forecast", {
                params: getParams(lat, lng)
            });
        },

        getLocation: function () {
            return $http.get("http://localhost:5000/setup/pos/get");
        }
    };

}]);
