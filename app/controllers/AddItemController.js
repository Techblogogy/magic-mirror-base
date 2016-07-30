app.controller('AddCtr', ['$scope','$document', '$http', 'socket',function ($scope,$document,$http, socket) {
    $scope.loaded = function(){};
    $scope.page_id = "p_add";
    $scope.img = {
        cat: "res/pics/cat.jpg"
    };

    console.log("INIT");
    socket.emit("user_on_add");
    // http.post

    socket.forward('m_camera', $scope);
    $scope.$on("socket:m_camera", function (event, data) {
      	console.log("hello camera works");
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
    $scope.cam_data = {};
    socket.forward('m_camera_dat', $scope);
    $scope.$on("socket:m_camera_dat", function (event, data) {
        console.log(data);
        $scope.cam_data = data[0];
        $scope.$apply();

    });

    $scope.add_request = function(){
        $http.post('http://localhost:5000/wardrobe/add')
        };


    $scope.click = function(){
        console.log("CLICK 2");
        console.log(document.getElementById('message').style.display);
        // document.getElementById('message').style.display = 'none';
        if (document.getElementById('message').style.display == '' || document.getElementById('message').style.display == 'none'){
            document.getElementById('message').style.display = 'block';
        }
        else if (document.getElementById('message').style.display == 'block'){
            document.getElementById('message').style.display = 'none';
        }
        // socket.emit("start_loop");
        timer_html = "";
        $scope.add_request();
        setTimeout(function () {
            timer_html = "2";
            document.getElementById('timer').innerHTML = timer_html;
            console.log(timer_html);
        }, 1000);
        setTimeout(function () {
            timer_html = "1";
            document.getElementById('timer').innerHTML = timer_html;
            console.log(timer_html);
        }, 2000);
        setTimeout(function () {
            timer_html = "Capturing!";
            document.getElementById('timer').innerHTML = timer_html;
            console.log(timer_html);
        }, 3000);

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

    socket.forward('add_tags', $scope);
    $scope.$on("socket:add_tags", function (event, data) {
        console.log(data);
        tags_arr = "";
        for (var i = 0; i < data.length; i++) {
            if (i === data.length - 1) {
                tags_arr += data[i];
            }
            else{tags_arr += data[i]+","}
        }
        item_id = $scope.get_curitem_id();
        $http.post('http://localhost:5000/wardrobe/add/tags/'+item_id,{tags: tags_arr});


    });
}]);
