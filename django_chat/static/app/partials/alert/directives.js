angular.module('alert', [])
.directive('dAlerts', ['$rootScope', '$timeout', 'PATH', function($rootScope, $timeout, PATH) {
	return {
		restrict: 'A',
		templateUrl: PATH + 'partials/alert/alert.html',
		controller: function($scope, $rootScope, $timeout){
		    if (!$rootScope.alerts){
		        $rootScope.alerts = [];
		    }
			$scope.close_alert = function(index){
                $rootScope.alerts.splice(index, 1);
			};
			$rootScope.$watchCollection('alerts', function(newValue, oldValue, scope) {
			    if (scope.alerts.length >= 1){
                    $timeout(function(){
                        scope.alerts.splice(0, 1);
                    }, 3000);
			    }
            });
		}
	}
}]);