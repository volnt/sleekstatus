describe('PricingCtrl', function() {
  var PricingCtrl, $httpBackend, $scope, Auth = undefined;

  beforeEach(module('app'));
  beforeEach(function() {
    inject(function($controller, _$httpBackend_, _Auth_) {
      $scope = {};
      Auth = _Auth_;
      DashboardCtrl = $controller('PricingCtrl', { $scope: $scope, Auth: Auth});
      $httpBackend = _$httpBackend_;
    });
  });
  
  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });
  
  describe('main method', function() {
    it('should call $scope.fetchPlans', function() {
      $httpBackend.expectGET('/api/plan/basic').respond(200);
      $httpBackend.expectGET('/api/plan/big').respond(200);
      $httpBackend.expectGET('/api/plan/unlimited').respond(200);
      $httpBackend.flush();
      expect(true).toBe(true);
    });
  });  
});
