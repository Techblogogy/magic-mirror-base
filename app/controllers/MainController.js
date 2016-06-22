app.controller('MainController', ['$scope', '$location', 'socket', function ($scope, $location, socket) {

    $scope.anim = "";

    socket.emit("myevent", {lal: "string"});

    socket.forward('myresponse', $scope);
    $scope.$on('socket:myresponse', function (event, data) {
        console.log(data);

        $scope.switchView('weather', 'left_swipe');
    });

    $scope.switchView = function (view, animation) {
        $scope.$on('$locationChangeStart', function (event) {
            $scope.anim = animation;
        });
        $location.path(view);
    }
}]);
