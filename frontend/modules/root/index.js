module.exports = function(ngModule) {
  require("./partials/index.css");
  require("./chatservice.js")(ngModule);
  require("./chatTestController.js")(ngModule);
  require("./config.js")(ngModule);
};
