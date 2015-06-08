module.exports = function (ngModule) {
  ngModule.controller('chatTestController', function (chatService) {
    let vm = this;

    vm.data = chatService.data();

    vm.submitChat = () => {
      if (vm.chatInput) {
        chatService.sendMessage(vm.chatInput);
        vm.chatInput = "";
      }
    }

  });
};
