app.directive('uiWidgetMaps', function () {
    return {
        restrict: 'E',
        transclude: true,
        templateUrl: 'app/templates/widget.html',
        link: function ($scope) {
            $scope.initMap();
        }
    }
});
