app.controller('MainController', ['$scope', '$location', '$rootScope', function ($scope, $location, $rootScope) {

    $scope.anim = "";

    $scope.switchView = function (view, animation) {
        $scope.anim = animation;
        $location.path(view);
    }
}]);
