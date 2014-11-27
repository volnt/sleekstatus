app.controller("PricingCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth  = Auth;
  $scope.hashlib = new Rusha();

  $scope.login = function(email, password) {
    Auth.set(email, $scope.hashlib.digest(password));
    Auth.verify(function() {
      $location.url("/dashboard");
    }, function() {
      console.log("Error when logging in.");
    });
  }

  $scope.main = function() {
    /*
    * Entry point of the controller.
    */
    $scope.Auth.load();
    $(".navbar").addClass("navbar-default").removeClass("navbar-transparent");
  }();
});
