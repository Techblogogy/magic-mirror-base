app.controller('StlCtr', ['$scope','$document', function ($scope,$document) {
    $scope.loaded = function(){};
    $scope.page_id = "p_stylist";
    $scope.img = {
        cat: "res/pics/cat.jpg"
    };
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


    
}]);
