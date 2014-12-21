app.controller("MainCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth = Auth;

  $scope.backToTop = function() {
    $("body").animate({scrollTop: $("body").offset().top}, 'slow');
  };

  $scope.main = function() {
    /*
    * Entry point of the controller.
    */
  }();
});
