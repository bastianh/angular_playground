module.exports = function (ngModule) {

  ngModule.provider('navbarData', function () {
    var barItems = [];
    return {
      addMenu: function(data) {
        barItems.push(data);
      },
      $get: function () {
        return {
          barItems : barItems
        }
      }
    }
  });

  ngModule.directive('navbar', function () {
    return {
      restrict: 'E',
      scope: {},
      template: require("./navbar.html"),
      controllerAs: 'vm',
      controller: function ($scope, user, navbarData) {
        var vm = this;
        vm.barItems = navbarData.barItems;
        vm.user = user;
      }
    }
  })
};
