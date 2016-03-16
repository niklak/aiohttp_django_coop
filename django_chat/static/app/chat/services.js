angular.module('chat.services', ['ngResource'])
.constant('source_path', 'chat/')
.factory('Channel', ['$resource', 'source_path',
	function($resource, source_path){
		return $resource(source_path + 'channels/:pk/', {}, {
	        query: {method:'GET', params:{pk: null}, responseType:'json', isArray:true},
	        save: {method:'POST', responseType:'json'},
	});
}])
.factory('Message', ['$resource', 'source_path',
	function($resource, source_path){
		return $resource(source_path + 'channels/:pk/messages/', {}, {
	        query: {method:'GET', params:{pk: null}, responseType:'json', isArray:true}
	});
}])
.factory('RegUser', ['$resource', 'source_path',
	function($resource, source_path){
		return $resource(source_path + 'register/', {}, {
	        save: {method:'POST', responseType:'json',}
	});
}]);