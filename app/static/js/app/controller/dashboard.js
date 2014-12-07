app.controller("DashboardCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth = Auth;
  $scope.alerts = [];

  $scope.getAlerts = function() {
    $http.get("/api/alert").success(function(response) {
      $scope.alerts = response.alerts;
    }).error(function(response) {
      console.log("Error while fetching alerts.");
      if (response.code == 401) {
    	Auth.load();
      }
    });
  };

  $scope.addAlert = function(url) {
    var params = {
      email: $scope.Auth.get().email, 
      url : url
    };
    $http.post("/api/alert", params).success(function(response) {
      $scope.alerts.push(response);
    }).error(function(response) {
      console.log("Error : " + response.error);
      if (response.code == 401) {
	Auth.load();
      }
    });
  };

  $scope.deleteAlert = function(index) {
    $http.delete("/api/alert/"+$scope.alerts[index].sha).success(function(response) {
      $scope.alerts.splice(index, 1);
    }).error(function(response) {
      console.log("Error while fetching alerts.");
      console.log(response);
      if (response.code == 401) {
	Auth.load();
      }
    });
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
