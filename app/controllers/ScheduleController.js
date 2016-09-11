// Schedule Data Controller
app.controller('ScheduleCtr', ['$scope', '$http','socket',function ($scope, $http, socket) {
    $scope.plans = [];
    $scope.curr_plans_page = 0;
    $scope.name = "Plans for Today:";
    $scope.show_title = false;
    $scope.refresh = function(){
        $http.get('http://localhost:5000/gcal/today')
        .success(function(data){
            // console.log("DATA"+data);
            $scope.plans_num = data.length; //amount of plans
            $scope.plans_p_num = Math.floor($scope.plans_num/5); //amount of plans pages
            for(var i = 0; i <= $scope.plans_p_num; i++){ //for every page:
                $scope.plans[i] = [];//add 5 items from data, i - plans_page_number
                if ((i+1)*5 <= data.length){ //that's to avoid underfined stuff
                    for (var j = i*5 ; j < (i+1)*5; j++) {
                        $scope.plans[i].push(data[j]);
                    }
                } else {
                    for (var j = i*5 ; j < data.length; j++) {
                        $scope.plans[i].push(data[j]);
                    }
                }
            }
            console.log($scope.plans);
        });
    };

    $scope.loaded = function () {
      //handleAuthClick();
    };

    $scope.refresh();
    setInterval(function () {
        $scope.refresh();
    }, 60000);

    socket.forward('next_plans_page', $scope);
    $scope.$on("socket:next_plans_page", function(event, data){
        $scope.curr_plans_page += 1;
    });
    socket.forward('prev_plans_page', $scope);
    $scope.$on("socket:prev_plans_page", function(event, data){
        $scope.curr_plans_page -= 1;
    });

}]);
