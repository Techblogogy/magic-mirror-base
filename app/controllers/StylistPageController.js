var counter = 0;
app.controller('StlCtr', ['$scope','$document', '$http', 'socket',function ($scope,$document,$http, socket) {
    $scope.loaded = function(){};
    $scope.page_id = "p_stylist";
    $scope.img = {
        cat: "res/pics/cat.jpg"
    };

    // $scope.items =[
    //   {
    //     thumbnail: "res/pics/cat.jpg",
    //     f: 'MOVE',
    //     developer: 'MOVE, Inc.',
    //     price: 0.99
    //   }
    // ];

    // var counter2 = 0;
    $scope.switch_right = function(){
        // $document.find("current").removeClass("current");
        // x = angular.element(document.querySelectorAll(".current"));
        console.log(counter);
        counter += 1;
        // counter2 += 2;
        console.log(counter);
        if (counter < 4) {
            counter += 1;
            return;
        } else {
            counter = 0;
        }

        item_id = Number( angular.element( angular.element(document.querySelectorAll(".current"))[0] ).attr('it-id') );
        // console.log(item_id);
        angular.element(document.querySelectorAll("#item-"+item_id)).removeClass("current");
        // angular.element(document.querySelectorAll("current")).removeClass("current");
        item_id += 1;

        // console.log(item_id);
        angular.element(document.querySelectorAll("#item-"+item_id)).addClass("current");

        // angular.element(document.querySelectorAll("#item-{{x}}")).addClass("current");
    };
    $scope.switch_left = function(){
        // $document.find("current").removeClass("current");
        angular.element(document.querySelectorAll("#item-"+x)).removeClass("current");
        x -= 1
        if (x == 0) {
            x = 1;
        };
        angular.element(document.querySelectorAll("#item-"+x)).addClass("current");

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
        console.log("123");
        $scope.page_num +=1
        $scope.get_page_items($scope.page_num);

        angular.element(document.querySelectorAll("#item-"+x)).removeClass("current");
        x = $scope.page_num*9 +1;
        console.log(x);
        angular.element(document.querySelectorAll("#item-"+x)).addClass("current");
        // setTimeout(function () {
        //     angular.element(document.querySelectorAll("#item-"+x)).removeClass("current");
        //     x = $scope.page_num*9 +1;
        //     console.log(x);
        //     angular.element(document.querySelectorAll("#item-"+x)).addClass("current");
        // }, 1000);


        // angular.element(document.querySelectorAll("#item-{{x}}")).addClass("current");
    };


    var g_cn = 0;
    socket.forward('r_ctr', $scope);
    $scope.$on("socket:r_ctr", function (event, data) {
        g_cn++;
        console.log("GLOBAL:"+g_cn);
        // console.log(123456);
        if (data == "left") {
            $scope.switch_left();
        }
        else if (data == "right") {
            $scope.switch_right();
        }

        // $scope.switchView('weather', 'left_swipe');
    });

}]);
