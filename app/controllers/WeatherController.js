// Weather Data Controller
app.controller('WeatherCtr', ['$scope', '$http', 'socket',function ($scope, $http, socket) {

    $scope.name = "Weather";
    $scope.show_title = false;

    $scope.loaded = function () {};
    $scope.curr_weather = function () {$http.get('http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lng+'&units=metric&appid=ea1b2a690767c4cffc1832b89fe81d68')
    .then(function(d) {
        // Get weather data\
        console.log(d);
        $scope.w_dat.temp = d.data.main.temp;
        $scope.w_dat.icon = "res/icons/weather/"+d.data.weather[0].icon.slice(0,-1)+".png";
        $scope.w_dat.descr = d.data.weather[0].description;
    }, function (e) {});};

    $scope.get_min_max_weather = function(){
        $http.get('http://api.openweathermap.org/data/2.5/forecast?lat='+lat+'&lon='+lng+'&units=metric&appid=ea1b2a690767c4cffc1832b89fe81d68')
        .then(function(data) {
            console.log("WEATHER ARRAY 2222222");
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

    // navigator.geolocation.getCurrentPosition(function (p) {
    $http.get('http://localhost:5000/setup/pos/get')
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
        }
        else {
            rain_message = "It's not gonna rain today";
        }
        if ($scope.snow_counter > 0) {
            snow_message = "Snowy day";
        }
        else {
            snow_message = "";
        }
        document.getElementById('rain_message').innerHTML = rain_message;
        angular.element(document.querySelectorAll("#rain_message")).removeClass("msg");
        angular.element(document.querySelectorAll("#rain_message")).addClass("msg_active");
        document.getElementById('snow_message').innerHTML = snow_message;
        console.log(12345678);
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
