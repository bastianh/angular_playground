let angular = require("angular");
require("angular-bootstrap");
require("restangular");

let app = angular.module('app', [require("angular-ui-router"), 'ui.bootstrap', 'restangular']);

module.exports = app;

//noinspection JSUnresolvedVariable

require("./services")(app);

app.config(function ($compileProvider, socketProvider) {
  socketProvider.setUrl('http://192.168.33.12:9999/sockjs').setReconnect(5000);
  if (__DEV__) {
    // performance schub ;)
    $compileProvider.debugInfoEnabled(false);
  } else {
    console.warn("Development Mode!");
  }
});

require("./directives")(app);
require("./modules")(app);
