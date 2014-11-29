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
  .when("/about", {
    templateUrl: "about.html",
    controller: "AboutCtrl"
  })
  .when("/pricing", {
    templateUrl: "pricing.html",
    controller: "PricingCtrl"
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

app.factory('Auth', function($http, $location) {
  var is_authenticated = false;
  var user = {};
  
  var save = function() {
    if (!angular.isUndefined(user.email) && 
	!angular.isUndefined(user.password)) {
      sessionStorage.email = user.email;
      sessionStorage.password = user.password;
    }
  };
  
  var load = function(success, error) {
    var email = sessionStorage.email;
    var password = sessionStorage.password;
    if (angular.isUndefined(email) || angular.isUndefined(password)) {
      logout();
      if (typeof error == 'function') {
	error();
      }
    } else {
      verify(email, password, success, error);
    }
  };

  var login = function(email, password) {
    if (!email || !password) return ;
    var hashlib = new Rusha();

    verify(email, hashlib.digest(password), function() {
      $location.url("/dashboard");
    }, function() {
      console.log("Error when logging in.");
    });

  };

  var logout = function() {
    is_authenticated = false;
    user = {};
    sessionStorage.removeItem("email");
    sessionStorage.removeItem("password");
  };

  var verify = function(email, password, success, error) {
    $http.post('/api/user/login', {
      email: email, 
      password: password
    }).success(function(response) {
      is_authenticated = true;
      user = response;
      save();
      if (typeof success == "function") {
        success();
      }
    }).error(function() {
      logout();
      $location.url("/");
      if (typeof error == "function") {
        error();
      }
    });
  };
  
  var set_attribut = function(key, value) {
      user[key] = value;
  };

  var get_user = function() {
    return user;
  };

  return {
    is_authenticated: function() { return is_authenticated; },
    get: get_user,
    set: set_attribut,
    login: login,
    logout: logout,
    load: load,
    save: save,
    verify: verify,
  };
});
