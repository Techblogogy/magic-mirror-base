app.controller('MainController', ['$scope', '$location', 'socket', '$timeout','$document','$http',
function ($scope, $location, socket, $timeout,$document, $http) {

    $scope.curr_cmd = "";
    $scope.anim = "";
    $scope.bodge_time = 1; //in milliseconds


    // Switch View with an animation
    $scope.switchView = function (view, animation) {
        // $scope.anim = animation;

        $timeout(function () {
            $location.path(view);
        }, $scope.bodge_time);
    }

    // Help page stuff
    //Voice command to get list of VoiceCommands
    socket.forward('list_vcmd', $scope);
    $scope.$on("socket:list_vcmd", function (event, data) {
        document.getElementById('help').style.display = "block";
    });
    //CLOSE LIST OF VCs
    socket.forward('exit_context', $scope);
    $scope.$on("socket:exit_context", function (event, data) {
        document.getElementById('help').style.display = "none";
    });

    socket.forward('wake_up', $scope);
    $scope.$on("socket:wake_up", function (event, data) {
        document.getElementById('sleep_block').style.opacity = '0';
    });

    socket.forward('wardrobe_page', $scope);
    $scope.$on("socket:wardrobe_page", function (event, data) {
        $scope.switchView('stylist','left_swipe');
    });
    socket.forward('home_page', $scope);
    $scope.$on("socket:home_page", function (event, data) {
        $scope.switchView('','right_swipe');
    });

    //SLEEP
    socket.forward('sleep', $scope);
    $scope.$on("socket:sleep", function (event, data) {
        console.log(document.getElementById('sleep_block').style.opacity = '1');
        document.getElementById('sleep_block').style.opacity = '1';
    });

    // Microphone functions
    $scope.mic_active = function(){
    };
    $scope.mic_is_listening = function(){
    };
    $scope.audio_is_detected = function(){
        console.log("Command was detected");
    };

    $scope.default_microphone = function () {
        document.getElementById('m_listen').style.display = 'none';
        document.getElementById('m_detc').style.display = 'none';
        document.getElementById('microph_img').style.display = 'block';
    };


    socket.forward('audio_found', $scope);
    $scope.$on("socket:audio_found", function (event, data) {

        console.log("Microphone is listening");

        document.getElementById('m_detc').style.display = 'none';
        document.getElementById('microph_img').style.display = 'block';
        angular.element(document.querySelectorAll('.cssload-double-torus')).removeClass("blink");
        document.getElementById('m_listen').style.display = 'block';
    });

    socket.forward('audio_detected', $scope);
    $scope.$on("socket:audio_detected", function (event, data) {
        $scope.default_microphone();
        $scope.curr_cmd = data;
    });


    socket.forward('audio_error', $scope);
    $scope.$on("socket:audio_error", function (event, data) {
        $scope.default_microphone();
    });

    socket.forward('audio_uploading', $scope);
    $scope.$on("socket:audio_uploading", function (event, data) {
        angular.element(document.querySelectorAll('.cssload-double-torus')).addClass("blink");
    });

}]);
