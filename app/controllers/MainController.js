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
    // $http.post('http://localhost:5000/wardrobe/add', [])
    // .success(function(d){
    //     // $scope.items = d;
    //     console.log("sent thing");
    // });


    // Switch View with an animation
    $scope.switchView = function (view, animation) {
        $scope.anim = animation;

        $timeout(function () {
            $location.path(view);
        }, $scope.bodge_time);
    }

    socket.forward('wake_up', $scope);
    $scope.$on("socket:wake_up", function (event, data) {
        document.getElementById('sleep_block').style.opacity = '0';
    });

    socket.forward('wardrobe_page', $scope);
    $scope.$on("socket:wardrobe_page", function (event, data) {
        $scope.switchView('stylist','left_swipe');
    });
    socket.forward('home_page', $scope);
    $scope.$on("socket:home_page", function (event, data) {
        $scope.switchView('','right_swipe');
    });

    //SLEEP
    socket.forward('sleep', $scope);
    $scope.$on("socket:sleep", function (event, data) {
        console.log(document.getElementById('sleep_block').style.opacity = '1');
        document.getElementById('sleep_block').style.opacity = '1';
    });


}]);
