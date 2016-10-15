
app.factory("youtube", ['$http', function () {

    return {
        search: function (query) {
            return $http.get("http://localhost:5000/youtube", {
                params: {
                    "q": query
                }
            });
        }
    };

}]);
