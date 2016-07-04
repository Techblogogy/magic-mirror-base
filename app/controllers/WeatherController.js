// Weather Data Controller
app.controller('WeatherCtr', ['$scope', '$http', function ($scope, $http) {

    $scope.name = "Weather";
    $scope.show_title = false;

    $scope.loaded = function () {};

    navigator.geolocation.getCurrentPosition(function (p) {
            lat = p.coords.latitude;
            lng =  p.coords.longitude;



            // Get current weather
            $http.get('http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lng+'&units=metric&appid=ea1b2a690767c4cffc1832b89fe81d68')
                .then(function(data) {
                  console.log(data);

                  $scope.w_dat = {
                    temp: data.data.main.temp,
                    //min_temp: data.main.temp_min,
                    //max_temp: data.main.temp_max,
                    icon: "res/icons/weather/"+data.data.weather[0].icon+".png"
                  };
                  // data.weather[0].description = "thunderstorm"
                //   console.log(data.data.weather[0].icon);
                //   switch(data.data.weather[0].icon) {
                //       case "clear sky":
                //         $scope.w_dat.icon = "res/icons/weather/clear_sky.png";
                //         break;
                //       case "few clouds":
                //         $scope.w_dat.icon = "res/icons/weather/few_clouds.png";
                //         break;
                //       case "scattered clouds":
                //         $scope.w_dat.icon = "res/icons/weather/scattered_clouds.png";
                //         break;
                //       case "broken clouds":
                //         $scope.w_dat.icon = "res/icons/weather/broken_clouds.png";
                //         break;
                //       case "shower rain":
                //         $scope.w_dat.icon = "res/icons/weather/shower_rain.png";
                //         break;
                //       case "rain":
                //         $scope.w_dat.icon = "res/icons/weather/rain.png";
                //         break;
                //       case "thunderstorm":
                //         $scope.w_dat.icon = "res/icons/weather/thunderstorm.png";
                //         break;
                //       case "snow":
                //         $scope.w_dat.icon = "res/icons/weather/snow.png";
                //         break;
                //       case "mist":
                //         $scope.w_dat.icon = "res/icons/weather/mist.png";
                //         break;
                //       default:
                //         console.error("No icon found");
                //         break;
                //   }
              }, function (err) {

              });

              // Get min/max weather
              $http.get('http://api.openweathermap.org/data/2.5/forecast?lat='+lat+'&lon='+lng+'&units=metric&appid=ea1b2a690767c4cffc1832b89fe81d68')
                  .then(function(data) {
                      // console.log(data);
                      var graph = [];

                      var min_time = new Date();
                      var max_time = new Date(min_time.getFullYear(), min_time.getMonth(), min_time.getDate(), 23, 59).getTime();
                      // console.log(Math.floor(max_time/100));
                      for (var i=0; i<data.data.list.length; i++) {
                          if (data.data.list[i].dt <= Math.floor(max_time/1000)) {
                              graph.push(data.data.list[i].main.temp);
                          }
                      }

                      $scope.w_dat.min_temp = Math.min.apply(Math, graph);
                      $scope.w_dat.max_temp = Math.max.apply(Math, graph);
                  }, function (data) {

                  });
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
