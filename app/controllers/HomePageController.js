app.controller('HomePageController', ['$scope','socket','$http', function ($scope, socket, $http) {

    $scope.page_id = "p_home";



    socket.forward('add_page', $scope);
    $scope.$on("socket:add_page", function (event, data) {
        $scope.switchView('add','left_swipe');
    });

    //TUTORIAL
    socket.forward('tutorial', $scope);
    $scope.$on("socket:tutorial", function (event, data) {
        document.getElementById('tutorial').style.display = "block";
    });
    //CLOSE TUTORIAL
    socket.forward('tutorial_close', $scope);
    $scope.$on("socket:tutorial_close", function (event, data) {
        document.getElementById('tutorial').style.display = "none";
    });


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
    // GET IP
    $http.get('http://localhost:5000/setup/getip')
    .success(function(data){
        ip = data;
        $scope.ip = ip;
        console.log(ip);
    });
    // SETUP STATE
    $http.get('http://localhost:5000/gcal/isauth')
    .success(function(data){
        auth = data;
        console.log(auth.is_needed);
        if (auth.is_needed) {
            document.getElementById('auth_message').style.display = "none";
            return 0;
        }
        else {
            auth_message = "You need to setup your Magic Mirror";
            document.getElementById('auth_message').innerHTML = auth_message;
            document.getElementById('auth_message').style.display = "block";
        }
    });

    $http.get('http://localhost:5000/gcal/istblexist')
    .success(function(data){
        auth = data;
        console.log(auth.is_exist);
        if (auth.is_exist.length == 0) {
            auth_message = "Make sure you configured your calendars";
            document.getElementById('cal_message').innerHTML = auth_message;
            document.getElementById('cal_message').style.display = "block";
        }
        else {
            document.getElementById('cal_message').style.display = "none";
        }
    });
    $http.get('http://localhost:5000/setup/pos/isconf')
    .success(function(data){
        pos = data;
        console.log(pos.is_confirmed);
        if (pos.is_confirmed.length == 0) {
            pos_message = "Make sure you confirmed your position";
            document.getElementById('pos_message').innerHTML = pos_message;
            document.getElementById('pos_message').style.display = "block";
        }
        else {
            document.getElementById('pos_message').style.display = "none";
        }
    });
    // socket.forward('weather_warning', $scope);
    // $scope.$on("socket:weather_warning", function (event, data) {
    //     console.log("WEATHER WARNING");
    //     console.log($scope.w_dat.descr);
    //     w_message = "";
    //     w_message = $scope.w_dat.descr;
    //     document.getElementById('w_message').innerHTML = w_message;
    //     document.getElementById('w_message').style.display = "block";
    // });
    //


    socket.forward('r_ctr', $scope);
    $scope.$on("socket:r_ctr", function (event, data) {
        // g_cn++;
        // console.log("GLOBAL:"+g_cn);
      	console.log(123456);
        switch (data) {
            // case "left":
            //     $scope.switch_left();
            //     break;
            case "right":
                    $scope.switchView('stylist','left_swipe');
                    break;
            // case "up":
            //         $scope.switch_up();
            //         break;
            // case "down":
            //         $scope.switch_down();
            //         break;
            // case "click":
            //         $scope.click();
            //         break;
                break;
        }
        // $scope.switchView('weather', 'left_swipe');
    });
}]);
