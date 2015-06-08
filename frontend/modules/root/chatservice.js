let _ = require("lodash");

module.exports = function (ngModule) {
  ngModule.service('chatService', function ($rootScope, $http) {
    var service = this;
    var _data = {
      messages: [],
      userlist: {}
    };

    $rootScope.$on('socket-message', (e, message) => {
      if (message.type == 'chat') {
        _data.messages.push(message);
      }
      if (message.user_list) {
        _data.userlist = message.user_list;
      }
    });

    service.data = () => _data;

    service.sendMessage = (message) => {
      $http({
        method: "post",
        url: "chat/",
        data: {
          message: message
        }
      });

    }
  });
};
