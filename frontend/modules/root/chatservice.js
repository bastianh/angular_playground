module.exports = function (ngModule) {
  ngModule.service('chatService', function ($rootScope, $http) {
    var service = this;
    var _messages = [];
    var _userlist = {};

    $rootScope.$on('socket-message', (e, message) => {
      console.warn(typeof(message), message);
      if (message.type == 'chat') {
        _messages.push(message);
        console.log("add message");
      }
      console.log("messages", _messages);
    });

    service.messages = function () {
      return _messages;
    };

    service.sendMessage = (message) => {
      $http({
        method: "post",
        url: "chat/",
        data: {
          message:message
        }
      });

    }
  });
};
