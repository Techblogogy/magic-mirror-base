// Weather Data Controller
app.controller('WeatherCtr', ['$scope', '$http', 'socket', 'weather', function ($scope, $http, socket, weather) {

    $scope.name = "Weather";
    $scope.show_title = false;

    $scope.loaded = function () {};
    $scope.curr_weather = function () {

        weather.getWeather(lat, lng)
        .success(function(d) {
            $scope.w_dat.temp = d.main.temp;
            $scope.w_dat.icon = "res/icons/weather/"+d.weather[0].icon.slice(0,-1)+".png";
            $scope.w_dat.descr = d.weather[0].description;
        })
        .error(function (e) {
            console.error(e);
        });

    };

    $scope.get_min_max_weather = function(){

        weather.getForecast(lat, lng)
        .then(function(data) {
            console.log(data);
            // Extract data for today
            //variables
            var graph = []; // temperature graph

            var min_time = new Date();
            var max_time = new Date(min_time.getFullYear(), min_time.getMonth(), min_time.getDate(), 23, 59).getTime();
            console.log(max_time);
            $scope.rain_counter = 0;
            $scope.snow_counter = 0;
            for (var i=0; i<data.data.list.length; i++) {
                if (data.data.list[i].dt <= Math.floor((max_time+96000)/1000)) {
                    graph.push(data.data.list[i].main.temp);
                    $scope.w_dat.conditions = data.data.list[i].weather[0].id;
                    switch ($scope.w_dat.conditions%100) {
                        case 2:
                            $scope.rain_counter += 1;
                            break;
                        case 3:
                            $scope.rain_counter += 1;
                            break;
                        case 5:
                            $scope.rain_counter += 1;
                            break;
                        case 6:
                            $scope.snow_counter += 1;
                            break;
                        case 7:

                            break;
                        case 8:

                            break;
                        case 9:

                            break;
                    }
                }
            }
            // Add max/min variables to scope
            $scope.w_dat.min_temp = Math.min.apply(Math, graph);
            $scope.w_dat.max_temp = Math.max.apply(Math, graph);
            console.log($scope.w_dat.min_temp);
        });
    };

    weather.getLocation()
    .success(function(data){
        console.log(data);

        lat = data.lat;
        lng = data.lng;

        // Get current weather
        $scope.curr_weather();
        setInterval(function () {  $scope.curr_weather();}, 600000);

        // Get min/max weather
        $scope.get_min_max_weather();
        setInterval(function () { $scope.get_min_max_weather();}, 600000);

    });



    // Weather data placeholder
    $scope.w_dat = {
        temp: "res/icons/weather/loading.gif",
        min_temp: "res/icons/weather/loading.gif",
        max_temp: "res/icons/weather/loading.gif",
        icon: "" // Cloudy, Sunny, etc
    };

    socket.forward('weather_warning', $scope);
    $scope.$on("socket:weather_warning", function (event, data) {
        console.log("WEATHER WARNING");
        console.log($scope.w_dat.descr);

        rain_message = "";
        rain_message = $scope.w_dat.descr;

        if ($scope.rain_counter > 0) {
            rain_message = "You'd better take an umbrella";
        } else {
            rain_message = "It's not gonna rain today";
        }

        if ($scope.snow_counter > 0) {
            snow_message = "Snowy day";
        } else {
            snow_message = "";
        }

        document.getElementById('rain_message').innerHTML = rain_message;
        angular.element(document.querySelectorAll("#rain_message")).removeClass("msg");
        angular.element(document.querySelectorAll("#rain_message")).addClass("msg_active");
        document.getElementById('snow_message').innerHTML = snow_message;

        angular.element(document.querySelectorAll("#snow_message")).removeClass("msg");
        angular.element(document.querySelectorAll("#snow_message")).addClass("msg_active");
    });

    setTimeout(function () {
        angular.element(document.querySelectorAll("#rain_message")).removeClass("msg_active");
        angular.element(document.querySelectorAll("#rain_message")).addClass("msg");
        angular.element(document.querySelectorAll("#snow_message")).removeClass("msg_active");
        angular.element(document.querySelectorAll("#snow_message")).addClass("msg");
    }, 20000);


}]);

app.filter('tempC', function () {
    return function (input) {
        return input + "\xB0C";
    };
});
