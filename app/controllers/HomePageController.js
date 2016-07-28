app.controller('HomePageController', ['$scope', function ($scope) {

    $scope.page_id = "p_home";

    socket.forward('r_ctr', $scope);
    $scope.$on("socket:r_ctr", function (event, data) {
        // g_cn++;
        // console.log("GLOBAL:"+g_cn);
      	console.log(123456);
        switch (data) {
            // case "left":
            //     $scope.switch_left();
            //     break;
            case "right":
                    $scope.switchView('stylist','left_swipe');
                    break;
            // case "up":
            //         $scope.switch_up();
            //         break;
            // case "down":
            //         $scope.switch_down();
            //         break;
            // case "click":
            //         $scope.click();
            //         break;
                break;
        }
        // $scope.switchView('weather', 'left_swipe');
    });
}]);
