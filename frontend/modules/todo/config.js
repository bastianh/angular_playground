module.exports = function (ngModule) {

  ngModule.config(function ($stateProvider, navbarDataProvider) {

    navbarDataProvider.addMenu({
      state: 'todo',
      title: "Todo"
    });
    //
    // Now set up the states
    $stateProvider
      .state('todo', {
        url: "/todo",
        template: "<h1>TODO</h1>"
      })
  });

};
