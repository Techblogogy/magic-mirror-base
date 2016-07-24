app.controller('StlCtr', ['$scope','$document', '$http', 'socket',function ($scope,$document,$http, socket) {
    $scope.loaded = function(){};
    $scope.page_id = "p_stylist";
    $scope.img = {
        cat: "res/pics/cat.jpg"
    };

    console.log("INIT");

    $scope.switch_right = function(){

        item_id = Number( angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('it-id') );
        // console.log(item_id);
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        // angular.element(document.querySelectorAll("current")).removeClass("current");
        item_id += 1;
        if (item_id == $scope.page_num*9 +10) {
            $scope.next_page()

        }
        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
        console.log("it's"+item_id);
    };
    $scope.switch_left = function(){
        // $document.find("current").removeClass("current");
        item_id = Number( angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('it-id') );
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        item_id -= 1;
        if (item_id == $scope.page_num*9) {
            $scope.previous_page()
        }
        if (item_id == 0) {
            item_id = 1;
        };
        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");

        // angular.element(document.querySelectorAll("#item-{{x}}")).addClass("current");
    };

    // $scope.add_item();
    // $scope.get_page_items = function(p_num){
    //     $http.get('http://localhost:5000/wardrobe/get?items='+9+'&page='+p_num)
    //     .success(function(data){
    //         console.log(data);
    //         $scope.items = data;
    //         setTimeout(function () {
    //             console.log($document.find("#item-1"));
    //             $document.find("#item-1").addClass("current");
    //             angular.element(document.querySelectorAll("#item-1")).addClass("current");
    //         }, 1000);
    //     });
    //  };

    $scope.page_num = 0;
    $scope.get_page_items = function(p_num){
        $http.get('http://localhost:5000/wardrobe/get?items='+9+'&page='+p_num)
        .success(function(data){
            console.log(data);
            $scope.items = data;
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
        item_id = Number( angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('it-id') );
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
        item_id = Number( angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('it-id') );
        $scope.page_num -=1
        $scope.get_page_items($scope.page_num);
        console.log("pr"+item_id);
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");
    };

    $scope.click = function(){
        if (document.getElementById('parent_popup').style.display === 'none'){

            // document.querySelectorAll(".current")[0].style.margin = '100px';
            angular.element(document.querySelectorAll('#popup')).append(document.querySelectorAll(".current")[0]);
            document.getElementById('parent_popup').style.display = 'inline';
            document.querySelectorAll(".current")[0].style.width = '100%' ;
            // document.querySelectorAll(".current")[0].style.position = 'fixed' ;

        }
        else {
            document.getElementById('parent_popup').style.display = 'none';
            document.querySelectorAll(".current")[0].style.width = '33.33333333%' ;
            // angular.element(document.querySelectorAll('#popup')).remove(document.querySelectorAll(".current")[0]);
        }

    };



    // var g_cn = 0;
    socket.forward('r_ctr', $scope);
    $scope.$on("socket:r_ctr", function (event, data) {
        // g_cn++;
        // console.log("GLOBAL:"+g_cn);
        // console.log(123456);
        switch (data) {
            case "left":
                $scope.switch_left();
                break;
            case "right":
                    $scope.switch_right();
                    break;
            case "up":
                    $scope.previous_page();
                    break;
            case "down":
                    $scope.next_page();
                    break;
            case "click":
                    $scope.show_closer();
                    break;
                break;
        }
        // $scope.switchView('weather', 'left_swipe');
    });

}]);
