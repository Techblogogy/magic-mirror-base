var app = angular.module("mirror-ui", ['ui.bootstrap','ngRoute','ngAnimate','btford.socket-io','angular-google-gapi']);

// Connect to Socket.IO Server
app.factory('socket', function (socketFactory) {
    // console.log(7890);
    var iosock = io.connect("http://localhost:5000/io");

    iosock = socketFactory({
        ioSocket: iosock
    });

    return iosock;
});

// Routes Configuration
app.config(function ($routeProvider) {
    $routeProvider
    .when('/add', {
        controller: 'HomePageController',
        templateUrl: 'app/views/home.html'
        // animation: 'left_swipe'
    })
    .when('/stylist', {
        controller: "StlCtr",
        templateUrl: 'app/views/stylist.html'
    })
    .when('/', {
        controller: "AddCtr",
        templateUrl: 'app/views/add.html'
    });
});
