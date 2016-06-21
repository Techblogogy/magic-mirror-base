// Schedule Data Controller
app.controller('ScheduleCtr', ['$scope', function ($scope) {

    $scope.name = "Todays Plans";
    $scope.show_title = true;

    $scope.plans = [
        {
            time_start: "12:00pm",
            time_end: "14:00pm",
            text: "Do some stuff"
        },

        {
            time_start: "15:00pm",
            time_end: "15:30pm",
            text: "Coffe with Dave"
        },

        {
            time_start: "16:00pm",
            time_end: "16:05pm",
            text: "Go have fun and this: antidisestablishmentarianism"
        }
    ];
}]);
