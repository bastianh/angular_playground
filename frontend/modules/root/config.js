module.exports = function (ngModule) {

  ngModule.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise("/");
    //
    // Now set up the states
    $stateProvider
      .state('index', {
        url: "/",
        template: "<h1>Index</h1> <div>{{ hi }}</div>",
        controller: function ($scope, socket) {
          $scope.hi = socket.status();
          console.log("xxx", $scope.hi);

          $scope.$on('socket-status', function (event, args) {
            $scope.hi = args.status;
          });

        }
      })
  });

};
