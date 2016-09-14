app.controller('AddCtr', ['$scope','$document', '$http', 'socket',function ($scope,$document,$http, socket) {
    $scope.loaded = function(){};
    $scope.page_id = "p_add";

    $scope.time_to_add_tags = false;

    socket.emit("user_on_add");
    setTimeout(function () {
        socket.emit("m_camera");
    }, 2000);
    setTimeout(function () {
        socket.emit("m_camera_dat");
    }, 4000);

    /* TODO: Were actuall adding begins */

    // Recieves and switches basic camera events
    socket.forward('m_camera', $scope);
    $scope.$on("socket:m_camera", function (event, data) {
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
            case "compression_begin":
            console.log("compression_begin");
            break;
            case "compression_off":
            console.log("compression_off");
            break;
        }
    });

    $scope.cam_data = {};

    $scope.state_one = true;
    $scope.state_two = false;
    // Recieves basic info about item
    socket.forward('m_camera_dat', $scope);
    $scope.$on("socket:m_camera_dat", function (event, data) {
        $scope.state_one = false;
        $scope.state_two = true;
        // Get data from json parser
        $scope.cam_data = JSON.parse(data)[0];
        console.log($scope.cam_data);
        document.getElementById('item_preview').style.display = 'block';
        $scope.time_to_add_tags = true;
        timer_html = "It's time to add some tags to your item, use voice command your tag words (you can add as many as you want)  + word 'tag' in the end";
        document.getElementById('timer').innerHTML = timer_html;
        console.log(timer_html);
        document.getElementById('timer').style.display = "block";

        $scope.$apply();

    });
    // SAVE TAGS OR NOT - THING FOR REMOTE CONTROL
    $scope.switch_right = function(){
        angular.element(document.querySelectorAll("#b_save")).removeClass("current");
        angular.element(document.querySelectorAll("#b_dont_save")).addClass("current");
    };
    $scope.switch_left = function(){
        angular.element(document.querySelectorAll("#b_dont_save")).removeClass("current");
        angular.element(document.querySelectorAll("#b_save")).addClass("current");

    };
//ALL MAGIC STARTS HERE
    // -----------------------STATE ONE STARTED -------------------------------
    $scope.user_clicked_save = false; // VARIABLE FOR SAVING TAGS
    $scope.click_counter = 0;   //MAGIC VARIABLE
    $scope.click_code = function(){
        if ($scope.click_counter == 0 && $scope.state_one) {
            $scope.video = true;
            // Hide info message
            document.getElementById('add_h2').style.display = 'none';
            document.getElementById('item_preview').style.display = 'none';
            if (document.getElementById('message').style.display == '' ||
            document.getElementById('message').style.display == 'none')
            {
                document.getElementById('message').style.display = 'block';
            }else if (document.getElementById('message').style.display == 'block')
            {
                document.getElementById('message').style.display = 'none';
            }
            document.getElementById('timer').style.display = "block";
            timer_html = "";
            socket.emit("record_start");
            $scope.click_counter += 1;

        } else if ($scope.click_counter == 1 && $scope.state_one) {
            socket.emit("record_stop");
            $scope.click_counter += 1;
            $scope.time_to_add_tags = true;
            timer_html = "Please wait, we are processing the information...";
            document.getElementById('timer').innerHTML = timer_html;
            console.log(timer_html);
            document.getElementById('timer').style.display = "block";
        }
        // -----------------------STATE ONE FINISHED -------------------------------

        // -----------------------STATE TWO STARTED -------------------------------
        if ($scope.state_two && $scope.click_counter == 2) {
            if (angular.element(document.querySelectorAll("#b_save")).hasClass("current")){
                document.getElementById('save_tags').style.display = 'none';
                document.getElementById('timer').innerHTML = "Click again to finish adding and go to wardrobe";

                $scope.user_clicked_save = true;

                item_id = $scope.super_id;
                tags_arr = $scope.super_tags;
                $http.post('http://localhost:5000/wardrobe/add/tags/'+item_id,{tags: tags_arr})
                .success(function (dat) {
                    console.log(dat);
                    $http.get('http://localhost:5000/wardrobe/get/item/'+item_id)

                    .success(function (dat) {
                        $scope.cam_data = dat[0];
                    }, function () {console.log("EROR"); });

                    setTimeout(function (){
                        $scope.$apply();
                    }, 1000);

                }, function () {console.log("EROR"); });
            } else {
                document.getElementById('save_tags').style.display = 'none';
                document.getElementById('timer').innerHTML = "Click again to finish adding and go to wardrobe";
            }
        // $scope.state_one = false;
        // $scope.state_two = true;
        $scope.click_counter += 1;
        }
        if ($scope.state_two && $scope.click_counter == 3) {
            $scope.video = false;
            // socket.emit("user_on_quit");
            socket.emit("user_on_leave");

            document.getElementById('item_preview').style.display = 'none';
            $scope.switchView('stylist','right_swipe');
        }
    }
    // -----------------------STATE TWO FINISHED -------------------------------


    // Adding tags event
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

    // Modify dresscode event
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
        $scope.click_code();
    });

    socket.forward('save_tags', $scope);
    $scope.$on("socket:save_tags", function (event, data) {
        $scope.click_code();
        $scope.state_two = true;
    });

    socket.forward('finish_tags', $scope);
    $scope.$on("socket:finish_tags", function (event, data) {
        $scope.click_code();
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
