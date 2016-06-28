// Weather Data Controller
app.controller('WeatherCtr', ['$scope', '$http', function ($scope, $http) {

    $scope.name = "Weather";
    $scope.show_title = false;

    $scope.loaded = function () {};

    navigator.geolocation.getCurrentPosition(function (p) {
            lat = p.coords.latitude;
            lng =  p.coords.longitude;

            $http.get('http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lng+'&units=metric&appid=ea1b2a690767c4cffc1832b89fe81d68')
                .success(function(data) {
                  console.log(data);

                  $scope.w_dat = {
                    temp: data.main.temp,
                    icon: ""
                  };

                  switch(data.weather[0].description) {
                      case "clear sky":
                        $scope.w_dat.icon = "res/icons/weather/clear_sky.png";
                        break;
                      case "few clouds":
                        $scope.w_dat.icon = "res/icons/weather/few_clouds.png";
                        break;
                      case "scattered clouds":
                        $scope.w_dat.icon = "res/icons/weather/scattered_clouds.png";
                        break;
                      case "broken clouds":
                        $scope.w_dat.icon = "res/icons/weather/broken_clouds.png";
                        break;
                      case "shower rain":
                        $scope.w_dat.icon = "res/icons/weather/shower_rain.png";
                        break;
                      case "rain":
                        $scope.w_dat.icon = "res/icons/weather/rain.png";
                        break;
                      case "thunderstorm":
                        $scope.w_dat.icon = "res/icons/weather/thunderstorm.png";
                        break;
                      case "snow":
                        $scope.w_dat.icon = "res/icons/weather/snow.png";
                        break;
                      case "mist":
                        $scope.w_dat.icon = "res/icons/weather/mist.png";
                        break;

                  }
                })
        });


    $scope.w_dat = {
        temp: 0,
        icon: "res/icons/weather/cloud.png" // Cloudy, Sunny, etc.
    };
}]);

app.filter('tempC', function () {
    return function (input) {
        return input + "\xB0C";
    };
});
