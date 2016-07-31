
app.controller('StlCtr', ['$scope','$document', '$http', 'socket'/*,'$location','$timeout'*/,function ($scope,$document,$http, socket/*,$location,$timeout*/) {
    $scope.loaded = function(){};
    $scope.page_id = "p_stylist";
    $scope.img = {
        cat: "res/pics/cat.jpg"
    };
    // $scope.anim = "";
    // $scope.bodge_time = 1; //in milliseconds

    $scope.item_per_page = 8;

    console.log("INIT");

    $scope.get_curitem_id = function(){
        return Number( angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('it-id') );

    };
    $scope.get_curitem_vid_id = function(){
        return Number( angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('it-id') );
    };


    // Microphone functions
    $scope.mic_active = function(){
        // document.getElementById('red').style.display = 'none';
        // document.getElementById('green').style.display = 'block';
    };
    $scope.mic_is_listening = function(){
        console.log("Microphone is listening");
        document.getElementById('m_detc').style.display = 'none';
        document.getElementById('m_listen').style.display = 'block';

    };
    $scope.audio_is_detected = function(){
        console.log("Command was detected");
        document.getElementById('m_listen').style.display = 'none';
        document.getElementById('m_detc').style.display = 'block';
    };

    $scope.switch_item = function (id) {

        item_id = $scope.get_curitem_id();
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");

        item_id = id;

        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
        console.log("[TB DEBUG Switched To]: "+item_id);
    }

    $scope.switch_right = function(){

        item_id = $scope.get_curitem_id();
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");

        item_id += 1;
        if (item_id == $scope.items.length+2) {
            $scope.next_page()
        }

        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
        console.log("it's"+item_id);
    };
    $scope.switch_left = function(){
        // $document.find("current").removeClass("current");
        item_id = $scope.get_curitem_id();
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        item_id -= 1;

        if (item_id == 0) {
            if ($scope.page_num !== 0)
                $scope.previous_page();

            item_id = 1;
        }
        // if (p_num == 0 && item_id == 0){
        //     item_id = 1;
        // }
        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");

        // angular.element(document.querySelectorAll("#item-{{x}}")).addClass("current");
    };
    $scope.switch_down = function(){

        item_id = $scope.get_curitem_id();
        // console.log(item_id);
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        // angular.element(document.querySelectorAll("current")).removeClass("current");
        item_id += 3;
        if (item_id >= $scope.page_num*$scope.item_per_page + $scope.item_per_page+1) {
            $scope.next_page()

        }
        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
        console.log("it's"+item_id);
    };

    $scope.switch_up = function(){

        item_id = $scope.get_curitem_id();
        // console.log(item_id);
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        // angular.element(document.querySelectorAll("current")).removeClass("current");
        item_id -= 3;// 11 - 3 = 8
        if (item_id <= 0){
            item_id = 1;
        }
        if (item_id <= $scope.page_num*$scope.item_per_page) {
            $scope.previous_page();
        }

        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
        console.log("it's"+item_id);
    };

    $scope.page_num = 0;
    $scope.get_page_items = function(p_num){
        $http.get('http://localhost:5000/wardrobe/get?items='+8+'&page='+p_num)
        .success(function(data){
            if (data.length === 0) {
                return 0;
            }
            $scope.items = data;

            // $scope.items.push({"element": 1});
            // var counter = 0;
            for (var i = 0; i < $scope.items.length; i++) {
                $scope.items[i].vid_id = $scope.items[i].id;
                $scope.items[i].number = i+1;

                // $scope.items[i]["id"] = p_num*9 + counter  ;
                // if ($scope.items[i]["number"] == 1) {
                //     $scope.items[i]["id"] = p_num*9 + 1 ;
                //     counter += 1;
                // }
                // counter += 1;
            }
            console.log($scope.items);
            // angular.element(document.querySelectorAll(".row")).children()
            // setTimeout(function () {
            //     console.log($document.find("#item-1"));
            //     // $document.find("#item-1").addClass("current");
            //     angular.element(document.querySelectorAll("#item-1")).addClass("current");
            // }, 1000);
        });
    };
    $scope.get_page_items(0);

    $scope.next_page = function(){
        // $document.find("current").removeClass("current");
        item_id = $scope.get_curitem_id();
        console.log("next "+item_id);
        console.log("123");
        $scope.page_num +=1
        $scope.get_page_items($scope.page_num);

        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
        // setTimeout(function () {
        //     angular.element(document.querySelectorAll("#item-"+x)).removeClass("current");
        //     x = $scope.page_num*9 +1;
        //     console.log(x);
        //     angular.element(document.querySelectorAll("#item-"+x)).addClass("current");
        // }, 1000);


        // angular.element(document.querySelectorAll("#item-{{x}}")).addClass("current");
    };

    $scope.previous_page = function(){
        item_id = $scope.get_curitem_id();
        $scope.page_num -=1;
        $scope.get_page_items($scope.page_num);
        console.log("pr"+item_id);
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
    };
    $scope.item_worn = function(){
        item_id = $scope.get_curitem_id();
        id_for_db = $scope.get_curitem_vid_id();

        console.log($scope.items[item_id].t_wears);
        $scope.items[item_id].t_wears += 1;
        console.log($scope.items[item_id].t_wears);

        $http.post('http://localhost:5000/wardrobe/wear/'+id_for_db)
        .then(function () {
            $scope.get_page_items($scope.page_num);
        }, function () {
            console.log("ADD ERROR!");
        });
        // location.reload();
    };

    // function getOffset(elem) {
    //     if (elem.getBoundingClientRect) {
    //         return getOffsetRect(elem);
    //     } else {
    //     return getOffsetSum(elem);
    //     }
    // };
    $scope.item_is_open = false;
    $scope.click = function(itm_num){
        voice = false;
        // (document.getElementById('parent_popup').style.display === 'none')
        // getOffset(document.getElementById('popup'));
        // getOffsetRect()
        // console.log( document.querySelectorAll('img_c').offset() );

        // document.querySelectorAll(".current")[0].style.margin = '100px';
        // big_item = document.querySelectorAll(".current")[0].innerHTML;
        if (!$scope.item_is_open) {
            // if (itm_num%9 == 0 ){
            //     // $location.path("/add")
            //     $scope.switchView('add','left_swipe')
            //     // socket.emit("user_on_add");
            //     return 0;
            // }

            // big_item = "";
            // if (voice) {
            //     // console.log(itm_num);
            //     actual_id = itm_num%9;
            //     if (actual_id == 0) {
            //         actual_id = 9
            //     }
            //     // console.log(actual_id);
            //     big_item = document.getElementById("item-"+(actual_id)).innerHTML;
            // } else {
            //     // console.log("READ COM");
            //
            //     big_item = document.getElementById("item-"+(itm_num)).innerHTML;
            // }


            $scope.switch_item(itm_num);
            it_id = $scope.get_curitem_id();
            vid_id = $scope.get_curitem_vid_id();

            if (it_id == $scope.items.length+1) {
                $scope.switchView('add','left_swipe')
                return;
            }

            big_item = document.getElementById("item-"+(it_id)).innerHTML;

            document.getElementById('parent_popup').innerHTML = big_item;
            console.log(big_item);
            document.getElementById('parent_popup').style.display = 'inline-block';

            // vid_id = angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('vid-id');
            console.log(vid_id);

            socket.emit("start_video", vid_id);
            $scope.item_is_open = true;

            // DEBUG timeout
            setTimeout(function () {
                $scope.click(null);
            }, 30000)

        } else {
            if (document.getElementById('parent_popup').style.display === 'inline-block'){
                document.getElementById('parent_popup').style.display = 'none';
                socket.emit("closed");
            }
            $scope.item_is_open = false;
        }
    };

    $scope.add_item = function() {

    };
    $scope.r_click = '';
    // var g_cn = 0;
    socket.forward('r_ctr', $scope);
    $scope.$on("socket:r_ctr", function (event, data) {
        // g_cn++;
        // console.log("GLOBAL:"+g_cn);
        console.log(123456);
        switch (data) {
            case "left":
            $scope.switch_left();
            break;
            case "right":
            $scope.switch_right();
            break;
            case "up":
            $scope.switch_up();
            break;
            case "down":
            $scope.switch_down();
            break;
            case "click":
            id = $scope.get_curitem_id();
            $scope.click(id);
            break;
        }
        // $scope.switchView('weather', 'left_swipe');
    });

    //socket.forward('right', $scope);
    //$scope.$on("socket:right", function (event, data) {
    //    console.log("RIGHT!!!");
    //    $scope.switch_right();
    //});

    //socket.forward('left', $scope);
    //$scope.$on("socket:left", function (event, data) {
    //                $scope.switch_left();
    //});

    socket.forward('fullscreen', $scope);
    $scope.$on("socket:fullscreen", function (event, data) {

        $scope.click(data, true);

    });

    socket.forward('close_item', $scope);
    $scope.$on("socket:close_item", function (event, data) {
        // $scope.close_item();
        $scope.click(null);

    });

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

    // socket.forward('mic_active', $scope);
    // $scope.$on("socket:mic_active", function (event, data) {
    //                 $scope.mic_active();
    //             });

    socket.forward('mic_is_listening', $scope);
    $scope.$on("socket:mic_is_listening", function (event, data) {
        $scope.mic_is_listening();
    });
    socket.forward('audio_detected', $scope);
    $scope.$on("socket:audio_detected", function (event, data) {
        $scope.audio_is_detected();
    });
    socket.forward('item_worn', $scope);
    $scope.$on("socket:item_worn", function (event, data) {
        $scope.item_worn();
        console.log('WORN');
    });



    // setTimeout(function () {
    //     $http.post('http://localhost:5000/wardrobe/add/tags/'+1,{tags: "tags,lags,bugs"});
    // }, 1000)

}]);
