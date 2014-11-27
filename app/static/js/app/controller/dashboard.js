app.controller("DashboardCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth = Auth;
  $scope.alerts = [];
  $scope.navtabs = {
    "alerts": true,
    "subscription": false
  };

  $scope.getAlerts = function() {
    $http.get("/api/alert").success(function(response) {
      $scope.alerts = response.alerts;
    }).error(function() {
      console.log("Error while fetching alerts.");
    });
  };

  $scope.addAlert = function(url) {
    if ($scope.alerts.length >= 10) {
      return ;
    }
    var params = {"auth": $scope.Auth.get(), "email": $scope.Auth.get().email, "url" : url};
    $http.post("/api/alert/create", params).success(function(response) {
      $scope.alerts.push(response);
    }).error(function() {
      console.log("Error while fetching alerts.");
    });
  };

  $scope.deleteAlert = function(index) {
    var params = {"auth": $scope.Auth.get(), "email": $scope.alerts[index].email, "url" : $scope.alerts[index].url};
    $http.post("/api/alert/delete", params).success(function(response) {
      $scope.alerts.splice(index, 1);
    }).error(function() {
      console.log("Error while fetching alerts.");
    });
  };

  $scope.toggleAlerts = function() {
    $scope.navtabs.alerts = true;
    $scope.navtabs.subscription = false;
  };

  $scope.toggleSubscription = function() {
    $scope.navtabs.alerts = false;
    $scope.navtabs.subscription = true;
  };

  $scope.main = function() {
    /*
    * Entry point of the controller.
    */
    $scope.Auth.load(function() {}, function() {
      $location.url("/");
    });
    $(".navbar").removeClass("navbar-transparent").addClass("navbar-default");
    $scope.getAlerts();
  }();
});
