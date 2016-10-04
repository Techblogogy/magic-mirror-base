
// app.directive('onLoopFinish', function ($timeout) {
//     return {
//         restrict: 'A',
//         link: function (scope, element, attr) {
//             if (scope.$last === true) {
//                 $timeout(function () {
//                     console.log("finnished ng-repleat");
//                     scope.$emit(attr.onLoopFinish);
//                 });
//             }
//         }
//     }
// });

app.controller('StlCtr', ['$scope','$document', '$http', 'socket'/*,'$location','$timeout'*/,function ($scope,$document,$http, socket/*,$location,$timeout*/) {
    $scope.loaded = function(){};
    $scope.page_id = "p_stylist";

    $scope.curr_cmd = "";
    $scope.user_search = false;

    $scope.item_per_page = 8;


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
        return Number( angular.element( angular.element(document.querySelectorAll(".current.item_stl") )[0] ).attr('it-id') );

    };

    $scope.get_curitem_vid_id = function(){
        return Number( angular.element( angular.element(document.querySelectorAll(".current.item_stl") )[0] ).attr('vid-id') );
    };

    $scope.switch_item = function (id) {

        item_id = $scope.get_curitem_id();
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");

        item_id = id;

        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
        console.log("[TB DEBUG Switched To]: "+item_id);
    }

    $scope.switch_right = function(){
        // $scope.items
        item_id = $scope.get_curitem_id();
        // console.log(item_id);
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        // angular.element(document.querySelectorAll("current")).removeClass("current");
        item_id += 1;
        // if (item_id == $scope.page_num*$scope.item_per_page + $scope.item_per_page+1) {
        // if (item_id == $scope.item_per_page+1) {
        if (item_id == $scope.items.length+2) {
            $scope.next_page()
        }
        if (item_id == $scope.items.length-1) {
            $scope.next_page()
        }
        if (item_id == $scope.items.length-4) {
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
        if (item_id == 3) {
            if ($scope.page_num !== 0)
            $scope.previous_page();

            item_id = 4;
        }
        if (item_id == 6) {
            if ($scope.page_num !== 0)
            $scope.previous_page();

            item_id = 7;
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
        console.log($scope.page_num*($scope.item_per_page+1)+1);
        if (item_id >= $scope.item_per_page+2) {
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
                angular.element(document.querySelectorAll("#item-1")).addClass("current");
                return 0;
            }
            for (var i = 0; i < data.length; i++) {
                // img_path = data[i].thumbnail.split('.')[0];
                // data[i].thumbnail = img_path + "_small.jpg";

                data[i].vid_id = data[i].id;
                data[i].number = i+1;
            }

            $scope.items = data;
        });
    };


    $scope.get_page_items(0);
    $scope.next_page = function(){
        // $document.find("current").removeClass("current");
        if ($scope.page_num !== $scope.p_amount) {
            console.log($scope.page_num);

            item_id = $scope.get_curitem_id();

            angular.element(document.querySelectorAll("#page-"+$scope.page_num)).removeClass("current");
            angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");

            $scope.page_num +=1

            if ($scope.user_search) {
                $scope.get_search_results($scope.page_num);
            } else {
                $scope.get_page_items($scope.page_num);
                // $scope.p_cnt +=1;
            }

            angular.element(document.querySelectorAll("#page-"+$scope.page_num)).addClass("current");
            angular.element(document.querySelectorAll("#item-1")).addClass("current");

        }
    };

    $scope.previous_page = function(){
        item_id = $scope.get_curitem_id();
        if ($scope.page_num !== 0) {
            angular.element(document.querySelectorAll("#page-"+$scope.page_num)).removeClass("current");
            if ($scope.user_search) {
                $scope.page_num -=1;
                $scope.get_search_results($scope.page_num);
            }
            else {
                item_id = $scope.get_curitem_id();
                $scope.page_num -=1
                $scope.get_page_items($scope.page_num);
            }
            angular.element(document.querySelectorAll("#page-"+$scope.page_num)).addClass("current");

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
            // $scope.get_page_items($scope.page_num);
            $scope.switchView('','right_swipe');
        }, function () {
            console.log("ADD ERROR!");
        });
    };


    $scope.item_is_open = false;
    $scope.click = function(itm_num){
        if ($scope.items == undefined) {
            $scope.switchView('add','left_swipe')
            return 0;
            console.log("HERE IT IS ");
        }

        voice = false;
        if (!$scope.item_is_open) {

            $scope.switch_item(itm_num);
            it_id = $scope.get_curitem_id();
            vid_id = $scope.get_curitem_vid_id();

            if (it_id == $scope.items.length+1) {
                $scope.switchView('add','left_swipe')
                return;
            }
            console.log(it_id);

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

    socket.forward('exit_context', $scope);
    $scope.$on("socket:exit_context", function (event, data) {
        $scope.click(null);

    });

    // socket.forward('search', $scope);
    // $scope.$on("socket:search", function (event, data) {
    // console.log(data);
    $scope.get_search_results = function(p_num){
        $http.get('http://localhost:5000/wardrobe/get/smart?q='+$scope.qry+'&items='+8+'&page='+p_num)
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

    socket.forward('show_all', $scope);
    $scope.$on("socket:show_all", function (event, data) {
        $scope.user_search = false;
        p_num = $scope.page_num;
        $scope.get_page_items(p_num);
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

    socket.forward('search', $scope);
    $scope.$on("socket:search", function (event, data) {
        console.log(data);
        $scope.user_search = true;

        $scope.qry = data[0];

        $scope.page_num = 1;
        $scope.get_search_results($scope.page_num);


    });

}]);

// Dymanically load images
function add_load_img(img) {
    var img_path = img.src;
    if (img_path.split("_").length == 2) {
        img_path = img_path.split('.')[0];
        img_path = img_path.split('_')[0];
        console.log(img_path);

        img.src = img_path + ".jpg";
    }
}
