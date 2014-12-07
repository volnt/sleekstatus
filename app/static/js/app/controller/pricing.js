app.controller("PricingCtrl", function($scope, $http, $routeParams, $location, Alert, Auth) {

  $scope.Alert = Alert;
  $scope.Auth  = Auth;

  $scope.plans = {};

  $scope.subscribe = function(plan) {
    plan.loader = {subscribe: true};

    try {
      var exp_array = $scope.form.expiration.split('/');
    } catch (e) {
      console.log("Error : expiration date format is invalid.");
      plan.loader.subscribe = false;
      return ;
    }
    if (exp_array.length != 2) {
      console.log("Error : expiration date format is invalid.");
      plan.loader.subscribe = false;
      return ;
    }

    Stripe.card.createToken({
      number: $scope.form.number,
      cvc: $scope.form.cvc,
      exp_month: exp_array[0],
      exp_year: exp_array[1]
    }, function(status, response) {
      if (response.error) {
	console.log("Error : " + response.error.message);
	plan.loader.subscribe = false;
      } else {
	var token = response.id;
	var params = { token: token };
	$http.post("/api/plan/"+plan.id, params).success(function(response) {
	  Auth.set('plan', response);
	  plan.loader.subscribe = false;
	  $(".modal").modal('hide');
	}).error(function(response) {
	  console.log("Error : " + response.error);
	  plan.loader.subscribe = false;
	});
      }
      $scope.$apply();
    });
  };

  $scope.unsubscribe = function(plan) {
    plan.loader = {unsubscribe: true};

    $http.delete("/api/plan/"+plan.id).success(function(response) {
      console.log("Success : " + response.success);
      plan.loader.unsubscribe = false;
      Auth.set('plan', null);
    }).error(function(response) {
      console.log("Error : " + response.error);
      plan.loader.unsubscribe = false;
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
