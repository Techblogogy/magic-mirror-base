// Google Maps Data controller
app.controller('MapsCtr', ['$scope', function ($scope) {

    $scope.name = "Google Maps";
    $scope.show_title = false;

    // $scope.$on("$viewContentLoaded", function () {
    // })

    $scope.loaded = function () {
        $scope.map = new google.maps.Map(document.getElementById('g_map'), {
            center: {lat: 0, lng: 0},
            disableDefaultUI: true,
            zoom: 20
        });
        $scope.map.set('styles', [
            {
                featureType: "all",
                stylers: [
                    { saturation: -100 }
                ]
            }
        ]);
        // $scope.m_info = new google.maps.InfoWindow({map: $scope.map});

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (p) {
                var pos = {
                    lat: p.coords.latitude,
                    lng: p.coords.longitude
                };

                $scope.map.setCenter(pos);
            })
        }
    }
        // $scope.initMap();
}]);
