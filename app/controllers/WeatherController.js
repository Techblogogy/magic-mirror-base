// Weather Data Controller
app.controller('WeatherCtr', ['$scope', function ($scope) {

    $scope.name = "Weather";
    $scope.show_title = false;

    $scope.w_dat = {
        temp: 20,
        icon: "icons/weather/cloud.png" // Cloudy, Sunny, etc.
    };
}]);

app.filter('tempC', function () {
    return function (input) {
        return input + "\xB0C";
    };
});
