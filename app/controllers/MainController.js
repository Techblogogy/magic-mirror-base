app.controller('MainController', ['$scope', '$location', 'socket', '$timeout', function ($scope, $location, socket, $timeout) {

    $scope.anim = "";

    socket.emit("myevent", {lal: "string"});

    socket.forward('myresponse', $scope);
    $scope.$on('socket:myresponse', function (event, data) {
        console.log(data);

        // $scope.switchView('weather', 'left_swipe');
    });

    $scope.switchView = function (view, animation) {
        $scope.anim = animation;

        // THIS IS BULLSHIT!!!! C'MON MAN THIS IS ABSOLUTELY SHIT.
        // THE WORST BODGE I EVER HAD TO MAKE, LIKE EVER.
        // YOU CAN'T MONITOR CLASS CHNAGES, SO YOU'VE GOT TO WAIT 1 FUCKING MILLISECOND
        // AND ONLY THEN CHANGE THE FLIPPING PATH
        // I'M DONE WITH THIS. BACK IN AN HOUR AFTER A RELAXING BICYCLE RIDE!
        $timeout(function () {
            $location.path(view);
        }, 1);

    }
}]);
