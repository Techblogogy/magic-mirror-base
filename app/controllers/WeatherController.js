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
        .then(function(d) {
            // console.log(d);

            // Get weather data
            $scope.w_dat.temp = d.data.main.temp;
            $scope.w_dat.icon = "res/icons/weather/"+d.data.weather[0].icon+".png"

        }, function (e) {});

        // Get min/max weather
        $http.get('http://api.openweathermap.org/data/2.5/forecast?lat='+lat+'&lon='+lng+'&units=metric&appid=ea1b2a690767c4cffc1832b89fe81d68')
        .then(function(data) {
            console.log(data);
            var graph = []; // temperature graph

            var min_time = new Date();
            var max_time = new Date(min_time.getFullYear(), min_time.getMonth(), min_time.getDate(), 23, 59).getTime();

            // Extract data for today
            for (var i=0; i<data.data.list.length; i++) {
                if (data.data.list[i].dt <= Math.floor(max_time/1000)) {
                    graph.push(data.data.list[i].main.temp);
                }
            }

            // Add max/min variables to scope
            $scope.w_dat.min_temp = Math.min.apply(Math, graph);
            $scope.w_dat.max_temp = Math.max.apply(Math, graph);
        }, function (e) {});
    });

    // Weather data placeholder
    $scope.w_dat = {
        temp: "res/icons/weather/loading.gif",
        min_temp: "res/icons/weather/loading.gif",
        max_temp: "res/icons/weather/loading.gif",
        icon: "" // Cloudy, Sunny, etc.
    };
}]);

app.filter('tempC', function () {
    return function (input) {
        return input + "\xB0C";
    };
});
