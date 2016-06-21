// Weather Data Controller
app.controller('WeatherCtr', ['$scope', function ($scope) {

    $scope.name = "Weather";

    $scope.weather_data = {
        temp: 20,
        type_icon: "clody" // Cloudy, Sunny, etc.
    };
}]);
