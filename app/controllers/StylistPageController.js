app.controller('StlCtr', ['$scope','$document', '$http',function ($scope,$document,$http) {
    $scope.loaded = function(){};
    $scope.page_id = "p_stylist";
    $scope.img = {
        cat: "res/pics/cat.jpg"
    };

    $scope.items =[
      {
        thumbnail: "res/pics/cat.jpg",
        f: 'MOVE',
        developer: 'MOVE, Inc.',
        price: 0.99
      }
    ];

    var x = 1;
    $scope.switch_right = function(){
        // $document.find("current").removeClass("current");
        angular.element(document.querySelectorAll("#item-"+x)).removeClass("current");
        x += 1;
        angular.element(document.querySelectorAll("#item-"+x)).addClass("current");

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
            setTimeout(function () {
                console.log($document.find("#item-1"));
                $document.find("#item-1").addClass("current");
                angular.element(document.querySelectorAll("#item-1")).addClass("current");
            }, 1000);
        });
     };
     $scope.get_page_items(0);

    $scope.next_page = function(){
        // $document.find("current").removeClass("current");
        console.log("123");
        $scope.page_num +=1
        $scope.get_page_items($scope.page_num);
        setTimeout(function () {
            angular.element(document.querySelectorAll("#item-"+x)).removeClass("current");
            x = $scope.page_num*9 +1;
            console.log(x);
            angular.element(document.querySelectorAll("#item-"+x)).addClass("current");
        }, 1000);


        // angular.element(document.querySelectorAll("#item-{{x}}")).addClass("current");
    };
}]);
