
app.controller('StlCtr', ['$scope','$document', '$http', 'socket'/*,'$location','$timeout'*/,function ($scope,$document,$http, socket/*,$location,$timeout*/) {
    $scope.loaded = function(){};
    $scope.page_id = "p_stylist";
    $scope.img = {
        cat: "res/pics/cat.jpg"
    };
    // $scope.anim = "";
    // $scope.bodge_time = 1; //in milliseconds
    $scope.curr_cmd = "";
    $scope.user_search = false;

    $scope.item_per_page = 8;

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



    // $scope.p_cnt = 0;
    $scope.getNumber = function(num) {
        return new Array(num);
    };
    $http.get('http://localhost:5000/wardrobe/pamount')
    .success(function(data){
        $scope.p_amount = Number(data);
        console.log($scope.p_amount);
    });
    console.log($scope.p_amount);

    console.log("INIT");

    $scope.get_curitem_id = function(){
        return Number( angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('it-id') );

    };
    $scope.get_curitem_vid_id = function(){
        return Number( angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('vid-id') );
    };


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

    $scope.switch_item = function (id) {


        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
        console.log("[TB DEBUG Switched To]: "+item_id);
    }
>>>>>>> 33857a67613f47cc8ab0aca4f4c372dbd62fcb13

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
        if ($scope.page_num !== $scope.p_amount) {
            angular.element(document.querySelectorAll("#page-"+$scope.page_num)).removeClass("current");
            if ($scope.user_search) {
                console.log($scope.page_num);
                angular.element(document.querySelectorAll("#page-"+$scope.page_num)).removeClass("current");
                item_id = $scope.get_curitem_id();
                $scope.page_num += 1;
                $scope.get_search_results($scope.page_num);
            }
            else {

                item_id = $scope.get_curitem_id();
                $scope.page_num +=1
                $scope.get_page_items($scope.page_num);
                // $scope.p_cnt +=1;
            }

            angular.element(document.querySelectorAll("#page-"+$scope.page_num)).addClass("current");

            angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
            angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");

        }
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
        if ($scope.page_num !== 0) {
            if ($scope.user_search) {
                $scope.page_num -=1;
                $scope.get_search_results($scope.page_num);
            }
            else {
                item_id = $scope.get_curitem_id();
                $scope.page_num -=1
                $scope.get_page_items($scope.page_num);
            }
            angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
            angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");

        }
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
        // $scope.get_page_items($scope.page_num);
    };

    // function getOffset(elem) {
    //     if (elem.getBoundingClientRect) {
    //         return getOffsetRect(elem);
    //     } else {
    //     }
    // };
    $scope.item_is_open = false;
    $scope.click = function(itm_num){
        voice = false;
        if (!$scope.item_is_open) {
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
           console.log("[VIDEO DEBUG] "+vid_id);

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
<<<<<<< HEAD

=======
>>>>>>> 33857a67613f47cc8ab0aca4f4c372dbd62fcb13

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
    socket.forward('next_page', $scope);
    $scope.$on("socket:next_page", function (event, data) {
        $scope.next_page();
    });
    socket.forward('previous_page', $scope);
    $scope.$on("socket:previous_page", function (event, data) {
        $scope.previous_page();
    });

    socket.forward('fullscreen', $scope);
    $scope.$on("socket:fullscreen", function (event, data) {

        $scope.click(data, true);

    });

    socket.forward('close_item', $scope);
    $scope.$on("socket:close_item", function (event, data) {
        $scope.click(null);

    });

    // socket.forward('search', $scope);
    // $scope.$on("socket:search", function (event, data) {
    // console.log(data);
    $scope.get_search_results = function(p_num){
        $http.get('http://localhost:5000/wardrobe/get/smart?q='+q+'&items='+8+'&page='+p_num)
        .success(function(data){
            console.log(data);
            if (data.length === 0) {
                return 0;
            }
            $scope.items = data;
            // setTimeout(function () {
            //     $scope.$apply();
            // }, 50);
            for (var i = 0; i < $scope.items.length; i++) {
                    $scope.items[i].vid_id = $scope.items[i].id;
                    $scope.items[i].number = i+1;
            };
            // $scope.items.push({"element": 1});
            // var counter = 0;
        }, function () {console.log("EROR")});
    };
    // setTimeout(function () {
    //     p_num = $scope.page_num;
    //     q = "";
    //     q = "clubwear"
    //     $scope.user_search = true;
    //     $scope.get_search_results(p_num);
    //     // q = data;
    //     // console.log(q);
    // }, 5000);

    socket.forward('show_all', $scope);
    $scope.$on("socket:show_all", function (event, data) {
        $scope.user_search = false;
        p_num = $scope.page_num;
        $scope.get_page_items(p_num);
    });




    // });

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
        $scope.curr_cmd = data;
    });
    socket.forward('item_worn', $scope);
    $scope.$on("socket:item_worn", function (event, data) {
        $scope.item_worn();
        console.log('WORN');
    });

    socket.forward('add_page', $scope);
    $scope.$on("socket:add_page", function (event, data) {
        $scope.switchView('add','left_swipe');
    });



    // setTimeout(function () {
    //     $http.post('http://localhost:5000/wardrobe/add/tags/'+1,{tags: "tags,lags,bugs"});
    // }, 1000)

}]);
