// Weather Data Controller
app.controller('WeatherCtr', ['$scope', '$http', 'socket',function ($scope, $http, socket) {

    $scope.name = "Weather";
    $scope.show_title = false;

    $scope.loaded = function () {};
    $scope.curr_weather = function () {$http.get('http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lng+'&units=metric&appid=ea1b2a690767c4cffc1832b89fe81d68')
    .then(function(d) {
        // Get weather data\
        $scope.w_dat.temp = d.data.main.temp;
        $scope.w_dat.icon = "res/icons/weather/"+d.data.weather[0].icon+".png";
        $scope.w_dat.descr = d.data.weather[0].description;
    }, function (e) {});};
    $scope.get_min_max_weather = function(){
        $http.get('http://api.openweathermap.org/data/2.5/forecast?lat='+lat+'&lon='+lng+'&units=metric&appid=ea1b2a690767c4cffc1832b89fe81d68')
        .then(function(data) {
            console.log(data);
            // Extract data for today
            //variables
            var graph = []; // temperature graph

            var min_time = new Date();
            var max_time = new Date(min_time.getFullYear(), min_time.getMonth(), min_time.getDate(), 23, 59).getTime();

            for (var i=0; i<data.data.list.length; i++) {
                if (data.data.list[i].dt <= Math.floor(max_time/1000)) {
                    graph.push(data.data.list[i].main.temp);
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
        w_message = "";
        w_message = $scope.w_dat.descr;
        switch ($scope.w_dat.descr) {
            case "shower rain":
                w_message = "You'd better take an umbrella";
                break;
        };
        document.getElementById('w_message').innerHTML = w_message;
        document.getElementById('w_message').style.display = "block";
    });


}]);

app.filter('tempC', function () {
    return function (input) {
        return input + "\xB0C";
    };
});
