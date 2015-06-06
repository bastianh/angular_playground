let angular = require("angular");
let bootstrap = require("angular-bootstrap");
let app = angular.module('app', [require("angular-ui-router"), 'ui.bootstrap']);

module.exports = app;

if (!__DEV__) {
  console.info("Development Mode!");
}

require("./services")(app);
require("./directives")(app);
require("./modules")(app);

