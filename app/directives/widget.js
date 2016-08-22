app.directive('uiWidget', function () {
    return {
        restrict: 'E',
        transclude: true,
        templateUrl: 'app/templates/widget.html',
        link: function ($scope) {
            $scope.loaded();
        }
    }
});
