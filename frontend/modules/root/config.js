module.exports = function (ngModule) {

  ngModule.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise("/");
    //
    // Now set up the states
    $stateProvider
      .state('index', {
        url: "/",
        template: require("./partials/index.html"),
        controllerAs: "vm",
        controller: 'chatTestController'
      })
  });

};
