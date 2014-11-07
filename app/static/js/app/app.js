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
  .when("/dashboard", {
    templateUrl: "dashboard.html",
    controller: "DashboardCtrl"
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

app.factory('Auth', function($http) {
  var is_authenticated = false;
  var auth = {};

  var save = function() {
    localStorage.setItem('auth', JSON.stringify(auth));
  };

  var load = function(success, error) {
    auth = JSON.parse(localStorage.getItem('auth'));
    if (!auth) {
      logout();
    } else {
      verify(success, error);
    }
  };

  var logout = function() {
    is_authenticated = false;
    auth = {};
    save();
  };

  var verify = function(success, error) {
    $http.post('/api/user/login', auth).success(function(response) {
      is_authenticated = true;
      save();
      if (!angular.isUndefined(success)) {
        success();
      }
    }).error(function() {
      logout();
      if (!angular.isUndefined(error)) {
        error();
      }
    });
  };

  return {
    is_authenticated: function() { return is_authenticated; },
    get: function() { return auth; },
    set: function(email, password) { auth = {"email": email, "password": password}; },
    logout: logout,
    load: load,
    save: save,
    verify: verify,
  };
});
