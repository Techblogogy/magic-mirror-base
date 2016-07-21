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
    $scope.add_item = function(){
        $scope.clth = [];
        $http.post('http://localhost:5000/wardrobe/add',$scope.clth)
        .success(function(d){
            $scope.items = d;
            console.log(d);
        });
    };

    // $scope.add_item();
    $scope.get_page_items = function(){
    $http.get('http://localhost:5000/wardrobe/get?items='+9+'&page='+0)
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
 $scope.get_page_items();
 $scope.next_page = function(){
     // $document.find("current").removeClass("current");
     $scope.get_page_items();

     // angular.element(document.querySelectorAll("#item-{{x}}")).addClass("current");
 };

}]);
