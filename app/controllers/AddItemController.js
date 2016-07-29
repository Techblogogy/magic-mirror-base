app.controller('AddCtr', ['$scope','$document', '$http', 'socket',function ($scope,$document,$http, socket) {
    $scope.loaded = function(){};
    $scope.page_id = "p_add";
    $scope.img = {
        cat: "res/pics/cat.jpg"
    };

    console.log("INIT");

    socket.forward('m_camera', $scope);
    $scope.$on("socket:m_camera", function (event, data) {
        // g_cn++;
        // console.log("GLOBAL:"+g_cn);
      	console.log(hello camera works);
        switch (data) {
            case "cam_on":
                console.log('camera on');
                break;
            case "preview_on":
                console.log('preview_on');
                break;
            case "thumb_captured":
                console.log('thumb_captured');
                break;
            case "video_start":
                console.log("video_start");
                break;
            case "video_end":
                console.log("video_end");
                break;
            case "preview_off":
                console.log("preview_off");
                break;
            case "cam_off":
                console.log("cam_off");
                break;
            break;
            case "compression_begin":
                console.log("compression_begin");
                break;
            break;
            case "compression_off":
                console.log("compression_off");
                break;
            break;
        }
        // $scope.switchView('weather', 'left_swipe');
    });

    socket.forward('m_camera_dat', $scope);
    $scope.$on("socket:m_camera_dat", function (event, data) {
        console.log(data);
    });

    $scope.add_request = function(){
        $http.post('http://localhost:5000/wardrobe/add')
        };
    $scope.add_request();

    $scope.switch_right = function(){
    };
    $scope.switch_right = function(){
    };
    $scope.switch_right = function(){
    };
    $scope.switch_right = function(){
    };
    $scope.switch_right = function(){
    };
    $scope.switch_right = function(){
    };

}]);
