app.controller("IndexCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth  = Auth;
  $scope.Error = {};

  $scope.tryLogin = function(email, password) {
    Auth.login(email, password, function() {
      $scope.Error.login = {
        message: "The password looks incorrect."
      };
    });
  }
  
  $scope.main = function() {
    /*
    * Entry point of the controller.
    */
    $scope.Auth.load();
    $(".navbar").removeClass("navbar-default").addClass("navbar-transparent");
  }();
});
