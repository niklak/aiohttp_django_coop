var auth = angular.module('auth.services', ['ngResource', 'ngCookies']);

auth.factory('Login', ['$resource',
	function($resource){
		return $resource('chat/login/', {}, {
			post: {method:'POST', responseType:'json'},
		});
	}
]);

auth.factory('Logout', ['$resource',
	function($resource){
		return $resource('chat/logout/', {}, {
			query: {method:'GET', responseType:'json'},
		});
	}
]);
auth.factory('Auth', ['$cookies', function($cookies){
	var auth = {};
	auth.get = function(key){
		return $cookies.getObject(key) ? $cookies.getObject(key) : null;
	};
	auth.set = function(token, username, id){
		$cookies.putObject('token', token);
		$cookies.putObject('l', username);
		$cookies.putObject('id', id);
		this.refresh();
	};
	auth.refresh = function(){
		this.token = this.get('token');
		this.username = this.get('l');
		this.id = this.get('id');
	};
	auth.remove = function(){
		$cookies.remove('token');
		$cookies.remove('l');
		$cookies.remove('id');
		this.refresh();
	};
	auth.token = auth.get('token');
	auth.username = auth.get('l');
	auth.id = auth.get('id');
	auth.is_authenticated = function(){
		return this.token !== null && this.username !== null;
	};
	return auth;
}]);


