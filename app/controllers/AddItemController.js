app.controller('AddCtr', ['$scope','$document', '$http', 'socket',function ($scope,$document,$http, socket) {
    $scope.loaded = function(){};
    $scope.page_id = "p_add";
    $scope.img = {
        cat: "res/pics/cat.jpg"
    };
    $scope.time_to_add_tags = false;
    console.log("INIT");
    socket.emit("user_on_add");
    // http.post

    // Microphone functions
    $scope.mic_active = function(){
        // document.getElementById('red').style.display = 'none';
        // document.getElementById('green').style.display = 'block';
    };
    $scope.mic_is_listening = function(){
        console.log("Microphone is listening");
        setTimeout(function () {
            document.getElementById('m_detc').style.display = 'none';
        }, 2000);
        setTimeout(function () {
            document.getElementById('m_listen').style.display = 'block';
        }, 3000);


    };
    $scope.audio_is_detected = function(){
        console.log("Command was detected");
        document.getElementById('m_listen').style.display = 'none';
        document.getElementById('m_detc').style.display = 'block';
    };

    socket.forward('mic_is_listening', $scope);
    $scope.$on("socket:mic_is_listening", function (event, data) {
        $scope.mic_is_listening();
    });
    socket.forward('audio_detected', $scope);
    $scope.$on("socket:audio_detected", function (event, data) {
        $scope.audio_is_detected();
    });


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

    // setTimeout(function () {
    //     $scope.cam_data = {t_wears: 13};
    //     $scope.$apply();
    //
    // }, 2000);


    socket.forward('m_camera_dat', $scope);
    $scope.$on("socket:m_camera_dat", function (event, data) {
        $scope.cam_data = JSON.parse(data)[0];
        console.log($scope.cam_data);
        $scope.$apply();

    });

    $scope.add_request = function(){
        $http.post('http://localhost:5000/wardrobe/add')
        .success(function (data){
            // $scope.cam_data = JSON.parse(data)[0];
            console.log(data);
            $scope.cam_data = (data)[0];
            console.log($scope.cam_data);
        });
        };

    $scope.switch_right = function(){
        angular.element(document.querySelectorAll("#b_save")).removeClass("current");
        angular.element(document.querySelectorAll("#b_dont_save")).addClass("current");
    };
    $scope.switch_left = function(){
        angular.element(document.querySelectorAll("#b_dont_save")).removeClass("current");
        angular.element(document.querySelectorAll("#b_save")).addClass("current");

    };

    $scope.user_clicked_save = false;
    $scope.click_counter = 0;
    $scope.click = function(){
        if ($scope.click_counter == 0 ){
            $scope.video = true;
            document.getElementById('item_preview').style.display = 'none';
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
            document.getElementById('timer').style.display = "block";
            timer_html = "";
            $scope.add_request();
            document.getElementById('add_h2').style.display = 'none';
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
            setTimeout(function () {
                document.getElementById('timer').style.display = "none";
            }, 4000);
            setTimeout(function () {
                document.getElementById('item_preview').style.display = 'block';
                socket.emit("user_on_leave");
                $scope.time_to_add_tags = true;
                timer_html = "It's time to add some tags to your item, use voice command your tag words (you can add as many as you want)  + word 'tag' in the end";
                document.getElementById('timer').innerHTML = timer_html;
                console.log(timer_html);
                document.getElementById('timer').style.display = "block";
                // document.getElementById('timer').
            }, 5000);
            $scope.click_counter += 1;
        }
        else if ($scope.click_counter == 1 ){
            if (angular.element(document.querySelectorAll("#b_save")).hasClass("current")){
                document.getElementById('save_tags').style.display = 'none';
                document.getElementById('timer').innerHTML = "Click again to finish adding and go to wardrobe";
                $scope.user_clicked_save = true;
                console.log('TRUUUUUUU');
                item_id = $scope.super_id;
                tags_arr = $scope.super_tags;
                $http.post('http://localhost:5000/wardrobe/add/tags/'+item_id,{tags: tags_arr})
                .success(function (dat) {
                    console.log(dat);
                    $http.get('http://localhost:5000/wardrobe/get/item/'+item_id)
                    .success(function (dat) {
                        $scope.cam_data = dat[0];
                        console.log(dat);
                    }, function () {console.log("EROR")});
                    setTimeout(function (){
                        $scope.$apply();
                        console.log('tasaaaaaa');
                    }, 1000);
                }, function () {console.log("EROR")}
            );
            }
            else {
                document.getElementById('save_tags').style.display = 'none';
                document.getElementById('timer').innerHTML = "Click again to finish adding and go to wardrobe";
            }

            $scope.click_counter += 1;
        }
        else{
            $scope.video = false;
            socket.emit("user_on_quit");
            document.getElementById('item_preview').style.display = 'none';
            $scope.switchView('stylist','right_swipe');
        }
    };
    $scope.super_id = 0;
    $scope.super_tags ="";
    socket.forward('add_tags', $scope);
    $scope.$on("socket:add_tags", function (event, data) {
        if ($scope.time_to_add_tags) {
            console.log(data);
            tags_arr = "";
            for (var i = 0; i < data.length; i++) {
                if (i === data.length - 1) {
                    tags_arr += data[i];
                }
                else{tags_arr += data[i]+","}
            }
            item_id = $scope.cam_data.id;
            console.log('ID ID ID ID'+item_id);

            timer_html = tags_arr;
            document.getElementById('timer').innerHTML = timer_html;
            console.log(timer_html);
            document.getElementById('save_tags').style.display = "block";
            $scope.super_id = item_id;
            $scope.super_tags =tags_arr;
            document.getElementById('save_tags').style.top = "100px";
        }
    });
    socket.forward('edit_dresscode', $scope);
    $scope.$on("socket:edit_dresscode", function (event, data) {
        console.log(data);
        dresscode = "";
        for (var i = 0; i < data.length; i++) {
            if (i === data.length - 1) {
                dresscode += data[i];
            }
            else{dresscode += data[i]+","}
        }
        item_id = $scope.cam_data.id;
        console.log('ID ID ID ID'+item_id);

        dc_html = dresscode;
        document.getElementById('timer').innerHTML = dc_html;
        document.getElementById('timer').innerHTML = dc_html;
        console.log(dc_html);
        ;
    });

    socket.forward('save_dc', $scope);
    $scope.$on("socket:save_dc", function (event, data) {
        dresscode = document.getElementById('timer').innerHTML;
        document.getElementById('dresscode').innerHTML = dresscode;
        item_id = $scope.cam_data.id;
        $http.post('http://localhost:5000/wardrobe/add/dresscode/'+item_id,{dresscode: dresscode})
        .success(function (dat) {
            console.log(dat);
            $http.get('http://localhost:5000/wardrobe/get/item/'+item_id)
            .success(function (dat) {
                $scope.cam_data = dat[0];
                console.log(dat);
            }, function () {console.log("EROR")});
            setTimeout(function (){
                $scope.$apply();
                console.log('tasaaaaaa');
            }, 1000);
        }), function () {console.log("EROR")}
    });


    socket.forward('start_cmd', $scope);
    $scope.$on("socket:start_cmd", function (event, data) {
        $scope.click();
    });

    socket.forward('save_tags', $scope);
    $scope.$on("socket:save_tags", function (event, data) {
        $scope.click();
    });

    socket.forward('finish_tags', $scope);
    $scope.$on("socket:finish_tags", function (event, data) {
        $scope.click();
    });

    socket.forward('left', $scope);
    $scope.$on("socket:finish_tags", function (event, data) {
        $scope.switch_left();
    });

    socket.forward('right', $scope);
    $scope.$on("socket:right", function (event, data) {
        $scope.switch_right();
    });

}]);
