app.controller("PricingCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth  = Auth;

  $scope.plans = {};

  $scope.subscribe = function(plan) {
    var exp_array = $scope.form.expiration.split('/');
    if (exp_array.length != 2) {
      console.log("Error : expiration date format is invalid.");
    }

    Stripe.card.createToken({
      number: $scope.form.number,
      cvc: $scope.form.cvc,
      exp_month: exp_array[0],
      exp_year: exp_array[1]
    }, function(status, response) {
      if (response.error) {
	console.log("Error : " + response.error.message);
      } else {
	var token = response.id;
	var params = { token: token };
	$http.post("/api/plan/"+plan.id, params).success(function(response) {
	  Auth.set('plan', response);
	}).error(function(response) {
	  console.log("Error : " + response.error);
	});
      }
    });
  };

  $scope.unsubscribe = function(plan) {
    // TODO : Get card token using Stripe.js
    $http.delete("/api/plan/"+plan.id).success(function(response) {
      console.log("Success : " + response.success);
      Auth.set('plan', null);
    }).error(function(response) {
      console.log("Error : " + response.error);
    });
  };

  $scope.fetchPlans = function() {
    var fetchPlan = function(id) {
      $http.get("/api/plan/"+id).success(function(response) {
	$scope.plans[id] = response;
      }).error(function(response) {
	console.log("Error : "+response.error);
      });
    };
    fetchPlan("basic");
    fetchPlan("big");
    fetchPlan("unlimited");
  };

  $scope.main = function() {
    /*
     * Entry point of the controller.
     */
    $scope.Auth.load();
    $scope.fetchPlans();
    $(".navbar").addClass("navbar-default").removeClass("navbar-transparent");
  }();
});
