var app = angular.module("mirror-ui", ['ui.bootstrap','ngRoute','ngAnimate']);

app.config(function ($routeProvider) {
    $routeProvider
    .when('/', {
        controller: 'HomePageController',
        templateUrl: 'app/views/home.html',
        animation: 'left_swipe'
    })
    .when('/weather', {
        controller: "WeatherPageController",
        templateUrl: 'app/views/large_weather.html'
    });
});
