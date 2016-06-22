app.controller('MainController', ['$scope', '$location', 'socket', function ($scope, $location, socket) {

    $scope.anim = "";

    socket.emit("myevent");

    $scope.switchView = function (view, animation) {
        $scope.$on('$locationChangeStart', function (event) {
            $scope.anim = animation;
        });
        $location.path(view);
    }
}]);
