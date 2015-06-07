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

    vm.refreshList = () => vm.todos = baseTodo.getList().$object;

    vm.add_todo = function () {
      baseTodo.post({task: vm.newtask}).then(function(obj) {
        console.log("Object saved OK", obj);
        vm.newtask="";
        vm.todos.push(obj);
      }, function() {
        console.log("There was an error saving");
      });
    };

  });


};
