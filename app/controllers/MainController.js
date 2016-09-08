app.controller('MainController', ['$scope', '$location', 'socket', '$timeout','$document','$http',
function ($scope, $location, socket, $timeout,$document, $http) {

    $scope.curr_cmd = "";
    $scope.anim = "";
    $scope.bodge_time = 1; //in milliseconds

    // socket.emit("myevent");

    // socket.forward('r_ctr', $scope);
    // $scope.$on("socket:r_ctr", function (event, data) {
    //     // console.log("HEY Mnan!");
    //     console.log(data);
    //     if (data == "left") {
    //         $scope.switch_left();
    //     }
    //     else if (data == "right") {
    //         $scope.switch_right();
    //     }
    //
    //     // $scope.switchView('weather', 'left_swipe');
    // });

    // $http.post("http://localhost:5000/");
    // $http.post('http://localhost:5000/wardrobe/add', [])
    // .success(function(d){
    //     // $scope.items = d;
    //     console.log("sent thing");
    // });


    // Switch View with an animation
    $scope.switchView = function (view, animation) {
        $scope.anim = animation;

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
    socket.forward('list_vcmd_close', $scope);
    $scope.$on("socket:list_vcmd_close", function (event, data) {
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
        // document.getElementById('red').style.display = 'none';
        // document.getElementById('green').style.display = 'block';
    };
    $scope.mic_is_listening = function(){
        console.log("Microphone is listening");
        setTimeout(function () {
            document.getElementById('m_detc').style.display = 'none';
            document.getElementById('microph_img').style.display = 'block';
        }, 2000);
        setTimeout(function () {
            document.getElementById('m_listen').style.display = 'block';
        }, 3000);


    };
    $scope.audio_is_detected = function(){
        console.log("Command was detected");
        document.getElementById('m_listen').style.display = 'none';
        document.getElementById('m_detc').style.display = 'block';
        document.getElementById('microph_img').style.display = 'none';
    };
    $scope.audio_was_recorded = function(){
        console.log("Command was detected");
        // document.getElementById('m_listen').style.color = 'red';
        document.getElementById('mic_cmd').style.display = 'block';
        // document.getElementById('microph_img').style.display = 'none';
    };


    socket.forward('mic_is_listening', $scope);
    $scope.$on("socket:mic_is_listening", function (event, data) {
        $scope.mic_is_listening();
    });
    socket.forward('audio_detected', $scope);
    $scope.$on("socket:audio_detected", function (event, data) {
        $scope.audio_is_detected();
        $scope.curr_cmd = data;
    });

    socket.forward('mic_record', $scope);
    $scope.$on("socket:mic_record", function (event, data) {
        setTimeout(function () {
            console.log("MIC_RECORD");
            $scope.curr_cmd = "recording...";
            $scope.audio_was_recorded();

        }, 2000);

    });

    socket.forward('mic_send', $scope);
    $scope.$on("socket:mic_send", function (event, data) {
        setTimeout(function () {
            console.log("MIC_SEND");
            $scope.curr_cmd = "Command was sent";
            console.log($scope.curr_cmd);
            document.getElementById('mic_cmd').style.display = 'block';


        }, 3000);

    });

}]);
