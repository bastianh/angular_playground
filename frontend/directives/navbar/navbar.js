module.exports = function (ngModule) {

  ngModule.provider('navbarData', function () {
    var barItems = [];
    return {
      addMenu: function (data) {
        barItems.push(data);
      },
      $get: function () {
        return {
          barItems: barItems
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
      controller: function ($rootScope, user, navbarData, socket) {
        socket.setupSocket();
        var vm = this;
        vm.connectStyle = {};
        vm.barItems = navbarData.barItems;
        vm.user = user;
        $rootScope.$on('socket-status', function (event, args) {
          switch (args.status) {
            case 'connecting':
              vm.connectStyle = {color: 'orange'};
              break;
            case 'open':
              vm.connectStyle = {color: 'green'};
              socket.sendMessage({user:user});
              break;
            case 'closed':
              vm.connectStyle = {color: 'red'};
              break;
          }
        });
      }
    }
  })
};
