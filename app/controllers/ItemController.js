app.controller('ItemCtr', ['$scope', '$document','$http', function($scope, $document, $http) {
    $scope.loaded = function(){};

    $scope.add_item = function(){
        $scope.clth = [];
        $http.post('http://localhost:5000/wardrobe/add',$scope.clth)
        .success(function(d){
            $scope.items = d;
            console.log(d);
        });
    };

    // $scope.page_num = 0;
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
    //  $scope.get_page_items(0);


}]);
