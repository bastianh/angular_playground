module.exports = function (ngModule) {

  ngModule.value('SockJS', require("sockjs-client"));
  ngModule.provider('socket', function () {
    let provider = this;
    provider.setUrl = function (url) {
      provider.url = url;
      return provider;
    };
    provider.setReconnect = function (reconnect) {
      provider.reconnect = reconnect;
      return provider;
    };

    provider.$get = ["SockJS", "$timeout", "$rootScope", function (SockJS, $timeout, $rootScope) {
      var self = this;
      var socket;
      var reconnect_promise;

      var setStatus = function(newStatus) {
        self.status = newStatus;
        $rootScope.$broadcast('socket-status', {status: newStatus});
      };

      var asyncAngularify = function (socket, callback) {
        return callback ? function () {
          var args = arguments;
          $timeout(function () {
            callback.apply(socket, args);
          }, 0);
        } : angular.noop;
      };

      self.setupSocket = function () {
        if (!self.url) return false;
        if (socket) {
          socket.close();
        }
        socket = new SockJS(self.url);
        setStatus('connecting');

        socket.onopen = asyncAngularify(socket, function () {
          setStatus('open');
        });
        socket.onmessage = asyncAngularify(socket, function (e) {
          console.log('message', e.data);
          $rootScope.$broadcast('socket-message', {data: e.data});
        });
        socket.onclose = asyncAngularify(socket, function () {
          setStatus('closed');
          if (self.reconnect) {
            $timeout.cancel(reconnect_promise);
            reconnect_promise = $timeout(self.setupSocket, self.reconnect);
          }
        });
        return true;
      };

      return {

        status: () => self.status || "closed!",
        setupSocket: self.setupSocket
      }
    }];
  });

};
