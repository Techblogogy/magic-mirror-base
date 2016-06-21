var app = angular.module("mirror-ui", ['ui.bootstrap','ngRoute','ngAnimate']);

app.config(function ($routeProvider) {
    $routeProvider
    .when('/', {
        controller: 'MainController',
        templateUrl: 'app/views/home.html'
    })
    .when('/weather', {
        controller: "MainController",
        templateUrl: 'app/views/large_weather.html'
    });
});
