// Schedule Data Controller
app.controller('ScheduleCtr', ['$scope', function ($scope) {

    $scope.name = "Todays Plans";

    $scope.plans = [
        {
            time: "12:00pm - 14:00pm",
            text: "Do some stuff"
        },

        {
            time: "15:00pm - 15:30pm",
            text: "Coffe with Dave"
        },

        {
            time: "16:00pm - 16:05pm",
            text: "Go have fun and this: antidisestablishmentarianism"
        }
    ];
}]);
