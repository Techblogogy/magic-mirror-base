var app = angular.module("mirror-ui", ['ui.bootstrap','ngRoute','ngAnimate','btford.socket-io','angular-google-gapi']);

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
//weather
app.factory('forecast', ['$http', function($http) {

  var lat;
  var lng;

navigator.geolocation.getCurrentPosition(function (p) {
        lat = p.coords.latitude;
        lng =  p.coords.longitude;

        console.log(lat);
    });
    
  return $http.get('http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lng+'&units=metric&appid=ea1b2a690767c4cffc1832b89fe81d68')
            .success(function(data) {
              console.log(data);
              return data;

            })
            .error(function(err) {
              return err;
            });
}]);
