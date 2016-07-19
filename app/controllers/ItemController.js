app.controller('ItemCtr', ['$scope', function($scope) {
    $scope.items =[
      {
        icon: "res/pics/cat.jpg",
        title: 'MOVE',
        developer: 'MOVE, Inc.',
        price: 0.99
      },
      {
        icon: 'img/shutterbugg.jpg',
        title: 'Shutterbugg',
        developer: 'Chico Dusty',
        price: 2.99
      }
    ]
}]);
