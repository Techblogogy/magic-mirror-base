var app = angular.module("mirror-ui", ['ui.bootstrap','ngRoute','ngAnimate','btford.socket-io']);

// Connect to Socket.IO Server
app.factory('socket', function (socketFactory) {
    var iosock = io.connect("http://127.0.0.1:5000/io");

    iosock = socketFactory({
        ioSocket: iosock
    });

    return iosock;
});

// Routes Configuration
app.config(function ($routeProvider) {
    $routeProvider
    .when('/', {
        controller: 'HomePageController',
        templateUrl: 'app/views/home.html'
        // animation: 'left_swipe'
    })
    .when('/weather', {
        controller: "WeatherPageController",
        templateUrl: 'app/views/large_weather.html'
    });
});
