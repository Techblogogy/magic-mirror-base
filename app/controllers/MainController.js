app.controller('MainController', ['$scope', '$location', 'socket', '$timeout','$document','$http',
function ($scope, $location, socket, $timeout,$document, $http) {

    $scope.anim = "";
    $scope.bodge_time = 1; //in milliseconds

    // socket.emit("myevent");

    // socket.forward('r_ctr', $scope);
    // $scope.$on("socket:r_ctr", function (event, data) {
    //     // console.log("HEY Mnan!");
    //     console.log(data);
    //     if (data == "left") {
    //         $scope.switch_left();
    //     }
    //     else if (data == "right") {
    //         $scope.switch_right();
    //     }
    //
    //     // $scope.switchView('weather', 'left_swipe');
    // });

    // $http.post("http://localhost:5000/");
    $http.post('http://localhost:5000/wardrobe/add', [])
    .success(function(d){
        // $scope.items = d;
        console.log("sent thing");
    });


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
