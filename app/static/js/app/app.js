var app = angular.module("app", ["ngRoute"]);

app.filter('safe', ['$sce', function($sce) {
  return (function(text) {
    return $sce.trustAsHtml(text);
  });
}]).filter('formatDate', function() {
  return (function(date) {
    var fDate = new Date(date);
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return (fDate.getDate() + " " + months[fDate.getMonth()] + " " + fDate.getFullYear());
  });
}).filter('startFrom', function() {
  return (function(input, start) {
    return input.slice(start);
  });
});

app.config(function($routeProvider) {
  $routeProvider
  .when("/", {
    templateUrl: "index.html",
    controller: "IndexCtrl"
  })
  .otherwise({redirectTo: '/'});
});

app.factory('Alert', function() {
  var success = "";
  var danger = "";
  
  return {
    getSuccess: function() {
      return success;
    },
    getDanger: function() {
      return danger;
    },
    setSuccess: function(message) {
      danger = "";
      success = message;
    },
    setDanger: function(message) {
      danger = message;
      success = "";
    },
    reset: function() {
      danger = "";
      success = "";
    }
  };
});
