let angular = require("angular");
require("angular-bootstrap");
require("restangular");

let app = angular.module('app', [require("angular-ui-router"), 'ui.bootstrap', 'restangular']);
module.exports = app;

angular.element(document).ready(function () {
  angular.bootstrap(document, [app.name], {
    //strictDi: true
  });
});
require("./services")(app);

app.config(function ($compileProvider, socketProvider) {
  if (__DEV__) {
    // performance schub ;)
    socketProvider.setUrl(window.location.protocol+'//'+window.location.hostname+'/sockjs').setReconnect(5000);
    $compileProvider.debugInfoEnabled(false);
  } else {
    socketProvider.setUrl(window.location.protocol+'//'+window.location.hostname+':9999/sockjs').setReconnect(5000);
    console.warn("Development Mode!");
  }
});

require("./directives")(app);
require("./modules")(app);
