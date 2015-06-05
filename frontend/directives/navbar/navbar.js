module.exports = function (ngModule) {
  ngModule.directive('navbar', function () {
    return {
      restrict: 'E',
      scope: {},
      template: require("./navbar.html"),
      controllerAs: 'vm',
      controller: function () {
        var vm = this;
        vm.greeting = 'hello world!';
      }
    }
  })
};
