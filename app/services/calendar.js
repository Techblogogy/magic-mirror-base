
app.factory("calendar", ["$http", function ($http) {

    return {
        getToday: function () {
            return $http.get("http://localhost:5000/gcal/today");
        }
    }

}]);
