let angular = require("angular");
let bootstrap = require("angular-bootstrap");
let app = angular.module('app', [require("angular-ui-router"), 'ui.bootstrap']);

module.exports = app;

//noinspection JSUnresolvedVariable
if (__DEV__) {
  app.config(['$compileProvider', function ($compileProvider) {
    $compileProvider.debugInfoEnabled(false);
  }]);
} else {
  console.warn("Development Mode!");
}

require("./services")(app);
require("./directives")(app);
require("./modules")(app);
