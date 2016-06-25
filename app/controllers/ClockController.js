app.controller('ClockCtr', ['$scope', '$timeout', function ($scope, $timeout) {
    $scope.name = "Clock";
    $scope.show_title = false;

    $scope.time = Date.now();
    $scope.tickInterval = 1000;
    
    $scope.loaded = function () {};

    var tick = function () {
        $scope.time = Date.now();
        $timeout(tick, $scope.tickInterval);
    }

    $timeout(tick, $scope.tickInterval);

}]);
