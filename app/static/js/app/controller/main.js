app.controller("MainCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth = Auth;

  $scope.main = function() {
    /*
    * Entry point of the controller.
    */
  }();
});
