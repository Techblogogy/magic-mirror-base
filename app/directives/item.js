app.directive('itemDir', function() {
  return {
    restrict: 'E',
    scope: {
      info: "="
    },
    templateUrl: 'app/directives/item.html'
  };
});
