app.controller("PricingCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth  = Auth;

  $scope.main = function() {
    /*
     * Entry point of the controller.
     */
    $scope.Auth.load();
    console.log($scope.Auth.is_authenticated())
    $(".navbar").addClass("navbar-default").removeClass("navbar-transparent");
  }();
});
