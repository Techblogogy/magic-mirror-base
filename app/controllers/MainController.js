app.controller('MainController', ['$scope', '$location', '$rootScope', function ($scope, $location, $rootScope) {

    $scope.anim = "";

    $scope.switchView = function (view, animation) {
        $scope.$on('$locationChangeStart', function (event) {
            $scope.anim = animation;
        });
        $location.path(view);
    }
}]);
