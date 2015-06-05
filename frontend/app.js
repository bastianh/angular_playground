let angular = require("angular");
let bootstrap = require("angular-bootstrap");
let app = angular.module('app', [require("angular-ui-router"), 'ui.bootstrap']);

module.exports = app;

if (!__DEV__) {
  console.info("Development Mode !");
}

require("./directives")(app);

app.config(function ($stateProvider, $urlRouterProvider) {
  //
  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("/state1");
  //
  // Now set up the states
  $stateProvider
    .state('state1', {
      url: "/state1",
      template: require("./partials/state1.html"),
      controller: function ($scope) {
        $scope.alerts = [
          {type: 'danger', msg: 'Oh snap! Change a few things up and try submitting again.'},
          {type: 'success', msg: 'Well done! You successfully read this important alert message.'}
        ];
        $scope.addAlert = function () {
          $scope.alerts.push({msg: 'Another alert!'});
        };

        $scope.closeAlert = function (index) {
          $scope.alerts.splice(index, 1);
        };
      }
    })
    .state('state1.list', {
      url: "/list",
      template: require("./partials/state1.list.html"),
      controller: function ($scope) {
        $scope.items = ["A", "List", "Of", "Items", __DEV__];
      }
    })
    .state('state2', {
      url: "/state2",
      template: require("./partials/state2.html")
    })
    .state('state2.list', {
      url: "/list",
      template: require("./partials/state2.list.html"),
      controller: require("./controller/state2.js")
    });
});
