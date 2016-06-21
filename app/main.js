var app = angular.module("mirror-ui", ['ui.bootstrap','ngRoute']);

app.config(function ($routeProvider) {
    $routeProvider
    .when('/', {
        controller: 'MainController',
        templateUrl: 'app/views/home.html'
    })
    .when('/weather', {
        controller: "WeatherCtr",
        templateUrl: 'app/views/large_weather.html'
    });
});
