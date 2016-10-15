

app.controller('YouTubeController', ['$scope', '$location', 'socket', '$timeout','$document',
function ($scope, $location, socket, $timeout, $document ) {

    $scope.loaded = function() { };
    $scope.page_id = "yt_page";

    $scope.video_id = "FmWjPoqEhzg";
    $scope.video_pars = {
        controls: 0,
        autoplay: 1
    };
    $scope.playVid = {};

    $scope.playVid = function () {
        $scope.playVid.playVideo();
    };
    $scope.stopVid = function () {
        $scope.playVid.stopVideo();
    };
    $scope.pauseVid = function () {
        $scope.playVid.pauseVideo();
    };


}]);
