app.controller('MainController', ['$scope', '$location', function ($scope, $location) {

    $scope.switchView = function (view) {
        console.log("Switching");
        $location.path(view);
    }

}]);
