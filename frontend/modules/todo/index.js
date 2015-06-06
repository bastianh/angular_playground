module.exports = function(ngModule) {
  require("./config.js")(ngModule);
  require("./todoListController.js")(ngModule);
};
