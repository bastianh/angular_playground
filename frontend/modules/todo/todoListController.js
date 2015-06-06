let _ = require("lodash");

module.exports = function (ngModule) {

  ngModule.controller('todoListController', function (Restangular) {
    var vm = this;
    var baseTodo = Restangular.all('todos/');

    vm.todos = baseTodo.getList().$object;

    vm.remove_todo = function (todo) {
      todo.remove().then(function () {
          vm.todos = _.without(vm.todos, todo);
        }
      )
    };

    vm.add_todo = function () {
      baseTodo.post({task: vm.newtask}).then(function() {
        console.log("Object saved OK");
        vm.newtask="";
        vm.todos = baseTodo.getList().$object; // vorest laden wir einfach die ganze liste neu...
      }, function() {
        console.log("There was an error saving");
      });
    };

  });


};
