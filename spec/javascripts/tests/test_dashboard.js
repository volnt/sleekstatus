describe('DashboardCtrl', function() {
  var DashboardCtrl, $httpBackend, $scope, alert, Auth = undefined;

  beforeEach(module('app'));
  beforeEach(function() {
    inject(function($controller, _$httpBackend_, _Auth_) {
      $scope = {};
      Auth = _Auth_;
      DashboardCtrl = $controller('DashboardCtrl', { $scope: $scope, Auth: Auth});
      $httpBackend = _$httpBackend_;
    });
    alert = function(id) {
      return {
	email: "user@host.ndd",
	url: "http://path.ndd/"+id,
	sha: new Rusha().digest("user@host.nddhttp://path.ndd/"+id)
      };
    };
  });
  
  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });
  
  describe('main method', function() {
    it('should call $scope.getAlerts', function() {
      $httpBackend.expectGET('/api/alert').respond(200, {alerts: [1, 2, 3]});
      $httpBackend.flush();
      expect(true).toBe(true);
    });
  });
  
  describe('getAlerts method', function() {
    it('should set the $scope.alerts array from /api/alert.', function() {
      $httpBackend.expectGET('/api/alert')
	.respond(200, {
	  alerts: [alert(1), alert(2), alert(3)]
	});
      $httpBackend.flush();
      expect($scope.alerts).toEqual([alert(1), alert(2), alert(3)]);
    });
  });

  describe('addAlert method', function() {
    it('should POST an url to /api/alert and push the response to the alerts', function() {
      $scope.Auth.set("email", "user@host.ndd");
      var url = "http://host.ndd/";
      $httpBackend.expectGET('/api/alert')
	.respond(200, {alerts: [alert(2)]});
      $scope.addAlert(url);
      $httpBackend.expectPOST('/api/alert', {email: "user@host.ndd", url: url})
	.respond(200, alert(1));
      $httpBackend.flush();
      expect($scope.alerts).toEqual([alert(2), alert(1)]);
    });
  });

  describe('deleteAlert method', function() {
    it('should delete an alert from the list', function() {
      $httpBackend.expectGET('/api/alert')
	.respond(200, {alerts: [alert(1), alert(2), alert(3)]});
      $httpBackend.flush();
      $httpBackend.expectDELETE('/api/alert/'+alert(2).sha)
	.respond(200);
      console.log($scope.alerts);
      $scope.deleteAlert(1);
      $httpBackend.flush();
      expect($scope.alerts).toEqual([alert(1), alert(3)]);
    });
  });
});
