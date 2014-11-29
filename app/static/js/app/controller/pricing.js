app.controller("PricingCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth  = Auth;

  $scope.subscribe = function(plan) {
    // TODO : Get card token using Stripe.js
    var token = "";
    var params = {
      token: token
    };
    $http.post("/api/plan/"+plan.id+"/subscribe", params).success(function(response) {
      console.log("Success : " + response.success);
      Auth.set('plan', plan.id);
    }).error(function(response) {
      console.log("Error : " + response.error);
    });
  };

  $scope.unsubscribe = function(plan) {
    // TODO : Get card token using Stripe.js
    var token = "";
    var params = {
      token: token
    };
    $http.post("/api/plan/"+plan.id+"/unsubscribe", params).success(function(response) {
      console.log("Success : " + response.success);
    }).error(function(response) {
      console.log("Error : " + response.error);
    });
  };

  $scope.main = function() {
    /*
     * Entry point of the controller.
     */
    $scope.Auth.load();
    $(".navbar").addClass("navbar-default").removeClass("navbar-transparent");
  }();
});
