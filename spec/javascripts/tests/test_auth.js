describe('AuthFactory', function() {
  var Auth = undefined;
  var $httpBackend = undefined;
  var user = undefined;

  beforeEach(module('app'));
  beforeEach(function()  {
    sessionStorage.clear();
    user = {
      email: "user@host.ndd",
      password: "password"
    };

    inject(function(_Auth_, _$httpBackend_) {
      Auth = _Auth_;
      $httpBackend = _$httpBackend_;
    });
  });

  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  describe('get method', function() {
    it('should return the user attributes', function() {
      expect(Auth.get()).toEqual({});
      Auth.set("email", user.email);
      Auth.set("password", user.password);
      
      expect(Auth.get()).toEqual(user);      
    });
  });

  describe('is_authenticated method', function() {
    it('should return true if the user is authenticated', function() {
      var clear_password = user.password;
      user.password = new Rusha().digest(user.password);
      Auth.login(user.email, clear_password);

      $httpBackend.expectPOST('/api/user/login', user).respond(200, user);
      $httpBackend.flush();
      expect(Auth.is_authenticated()).toBe(true);
    });
    it('should return false if the user is not authenticated', function() {
      expect(Auth.is_authenticated()).toBe(false);
    });
  });

  describe('set method', function() {
    it('should set a user attribute', function() {
      Auth.set("email", user.email);
      Auth.set("password", user.password);
      expect(Auth.get()).toEqual(user);
    });
  });

  describe('login method', function() {
    it('should authenticate if the credentials are valid', function() {
      var clear_password = user.password;
      user.password = new Rusha().digest(user.password);
      Auth.login(user.email, clear_password);

      $httpBackend.expectPOST('/api/user/login', user).respond(200, user);
      $httpBackend.flush();
      expect(Auth.is_authenticated()).toBe(true);
      expect(Auth.get()).toEqual(user);
      expect(sessionStorage.email).toBe(user.email);
      expect(sessionStorage.password).toBe(user.password);      
    });
    it('should not authenticate if the credentials are not valid', function() {
      var clear_password = user.password;
      user.password = new Rusha().digest(user.password);
      Auth.login(user.email, clear_password);

      $httpBackend.expectPOST('/api/user/login', user).respond(400);
      $httpBackend.flush();
      expect(Auth.is_authenticated()).toBe(false);
      expect(Auth.get()).toEqual({});
      expect(sessionStorage.email).not.toBeDefined();
      expect(sessionStorage.password).not.toBeDefined();
    });
  });

  describe('save method', function() {
    it('should save the users attributes in session if they are defined', function() {
      Auth.set("email", user.email);
      Auth.set("password", user.password);
      Auth.save();

      expect(sessionStorage.email).toBe(user.email);
      expect(sessionStorage.password).toBe(user.password);
    });
    it('should not save the users attributes in session if they are undefined', function() {
      Auth.save();

      expect(sessionStorage.email).not.toBeDefined();
      expect(sessionStorage.password).not.toBeDefined();
    });
  });

  describe('logout method', function() {
    it('should log out a logged in user', function() {
      var clear_password = user.password;
      user.password = new Rusha().digest(user.password);
      Auth.login(user.email, clear_password);
      $httpBackend.expectPOST('/api/user/login', user).respond(200, user);
      $httpBackend.flush();
      
      expect(Auth.is_authenticated()).toBe(true);
      
      Auth.logout();

      expect(Auth.is_authenticated()).toBe(false);
      expect(Auth.get()).toEqual({});
      expect(sessionStorage.email).not.toBeDefined();
      expect(sessionStorage.password).not.toBeDefined();    
    });
  });
});
