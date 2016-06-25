// Google Maps Data controller
app.controller('MapsCtr', ['$scope', function ($scope) {

    $scope.name = "Google Maps";
    $scope.show_title = false;

    // $scope.$on("$viewContentLoaded", function () {
    // })

    $scope.loaded = function () {
        console.log("INitin map");
        var maps = new google.maps.Map(document.getElementById('g_map'), {
            center: {lat: -34.397, lng: 150.644},
            zoom: 8
        });
    }
        // $scope.initMap();
}]);
