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
  socketProvider.setUrl(window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/sockjs').setReconnect(5000);
  if (__DEV__) {
    // performance schub ;)
    $compileProvider.debugInfoEnabled(false);
  } else {
    console.warn("Development Mode!");
  }
});

require("./directives")(app);
require("./modules")(app);
