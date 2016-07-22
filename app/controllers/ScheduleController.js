// Schedule Data Controller
app.controller('ScheduleCtr', ['$scope', '$http',function ($scope, $http) {

    $scope.name = "Plans for Today:";
    $scope.show_title = false;
    $scope.refresh = function(){
        $http.get('http://localhost:5000/gcal/today')
        .success(function(data){
            console.log(data);
            $scope.plans = data;

        });
    };

    $scope.loaded = function () {
      //handleAuthClick();
    };
    // $scope.refresh();
    setInterval(function () {
        $scope.refresh();
    }, 60000);

    // $scope.plans = [
    //     {
    //         time_start: "12:00pm",
    //         time_end: "14:00pm",
    //         text: "Do some stuff"
    //     },
    //
    //     {
    //         time_start: "15:00pm",
    //         time_end: "15:30pm",
    //         text: "Coffe with Dave"
    //     },
    //
    //     {
    //         time_start: "16:00pm",
    //         time_end: "16:05pm",
    //         text: "Go have fun and this: antidisestablishmentarianism"
    //     }
    // ];
}]);
