app.controller('ItemCtr', ['$scope', '$document','$http', function($scope, $document, $http) {
    $scope.loaded = function(){};
    $scope.items =[
      {
        thumbnail: "res/pics/cat.jpg",
        f: 'MOVE',
        developer: 'MOVE, Inc.',
        price: 0.99
      }
  ];
    $scope.x = 2;
    $scope.add_item = function(){
        $scope.clth = [];
        $http.post('http://localhost:5000/wardrobe/add',$scope.clth)
        .success(function(d){
            $scope.items = d;
            console.log(d);
        });
    };

    // $scope.add_item();

    $http.get('http://localhost:5000/wardrobe/get/all?items='+16+'&page='+0)
    .success(function(data){
        console.log(data);
        $scope.items = data;
        setTimeout(function () {
            console.log($document.find("#item-1"));
            $document.find("#item-1").addClass("current");
            angular.element(document.querySelectorAll("#item-1")).addClass("current");
        }, 1000);
    });
}]);
