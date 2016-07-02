app.controller('MainController', ['$scope', '$location', /*'socket',*/ '$timeout', function ($scope, $location, /*socket,*/ $timeout) {

    $scope.anim = "";
    $scope.bodge_time = 1; //in milliseconds

    // socket.emit("connected");

    // socket.forward('myresponse', $scope);
    // $scope.$on('socket:myresponse', function (event, data) {
    //     console.log(data);
    //
    //     $scope.switchView('weather', 'left_swipe');
    // });

    // Switch View with an animation
    $scope.switchView = function (view, animation) {
        $scope.anim = animation;

        // THIS IS BULLSHIT!!!! C'MON MAN THIS IS ABSOLUTELY SHIT.
        // THE WORST BODGE I EVER HAD TO MAKE, LIKE EVER.
        // YOU CAN'T MONITOR CLASS CHNAGES, SO YOU'VE GOT TO WAIT 1 FUCKING MILLISECOND
        // AND ONLY THEN CHANGE THE FLIPPING PATH
        // I'M DONE WITH THIS. BACK IN AN HOUR AFTER A RELAXING BICYCLE RIDE!
        // I'VE WAISTED HALF OF MY DAY TRYING TO DO THIS PROPERLY, AHHHHHHH!!!!
        $timeout(function () {
            $location.path(view);
        }, $scope.bodge_time);
    }


}]);
