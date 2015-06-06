module.exports = function (ngModule) {

  ngModule.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise("/");
    //
    // Now set up the states
    $stateProvider
      .state('index', {
        url: "/",
        template: "<h1>Index</h1>"
      })
  });

};
