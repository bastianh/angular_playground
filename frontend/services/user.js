module.exports = function(ngModule) {
  ngModule.service('user', function User() {
    var user = this;
    var metas = document.getElementsByTagName('meta');

    for (let i=0; i<metas.length; i++) {
      if (metas[i].getAttribute("property") == "user") {
        let data = angular.fromJson(metas[i].getAttribute("content"));
        angular.forEach(data, function(value, key) {
          user[key] = value;
        }, user);
        break;
      }
    }
  })
};
