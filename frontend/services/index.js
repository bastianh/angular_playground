module.exports = function(ngModule) {
  require("./socket.js")(ngModule);
  require("./user.js")(ngModule);
};
