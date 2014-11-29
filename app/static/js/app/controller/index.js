app.controller("IndexCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth  = Auth;

  $scope.main = function() {
    /*
    * Entry point of the controller.
    */
    $scope.Auth.load();
    $(".navbar").removeClass("navbar-default").addClass("navbar-transparent");
  }();
});
