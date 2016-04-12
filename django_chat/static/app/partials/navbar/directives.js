var navbar = angular.module('navbar', ['auth.services'])
.directive('dNavbar', ['$location','Login', 'Logout', 'Auth', '$uibModal', '$window', 'PATH',
						function($location, Login, Logout, Auth, $uibModal, $window, PATH) {
	return {
		restrict: 'A',
		templateUrl: PATH + 'partials/navbar/navbar.html',
		controller: function($scope, $rootScope, $location, Logout, Auth, $uibModal, $window, PATH){

			angular.element($window).bind('scroll', function() {
				$scope.change_class = (this.pageYOffset >= 100) ? true : false;
				$scope.$apply();
			});
			$scope.brand_text = 'Example chat';

			$scope.auth = Auth;

			$scope.logout = function(){
				$scope.r = Logout.query(function(r){
				    $rootScope.alerts.push({ type: 'info', msg: 'Goodbye, ' + Auth.username + '.'});
					$scope.auth.remove();
					$location.path('logout/');
				});
			}
			$scope.animationsEnabled = true;

			$scope.open = function () {

				var modalInstance = $uibModal.open({
					animation: $scope.animationsEnabled,
					templateUrl: PATH + 'partials/navbar/modal.html',
					controller: 'ModalInstanceCtrl',
					size: 'sm',
				});

				modalInstance.result.then(function (auth) {
					$scope.auth = auth;
                    $rootScope.alerts.push({ type: 'info', msg: 'Welcome, ' + auth.username + '!'});
                    $location.path('/');
				});
			};

			$scope.toggleAnimation = function () {
				$scope.animationsEnabled = !$scope.animationsEnabled;
			};
		}
	};
}])
.directive('socialLink', ['PATH', function(PATH){
    return {
        restrict: 'E',
        replace: true,
        templateUrl: PATH +'partials/navbar/social.html',
        scope: {backend:'=', icon:'='},
        link: function($scope, element, attrs){
            $scope.social_url = '/social/login/'+ $scope.backend + '/';
        },
    }
}]);
navbar.controller('ModalInstanceCtrl', ['$scope', '$uibModalInstance' , 'Login', 'Auth',
										function ($scope, $uibModalInstance, Login, Auth) {

	$scope.authenticate = function(u, p){
		$scope.r = Login.post({username: u, password: p },
			function(success){
				$scope.error = null;
				Auth.set(success.token, success.username, success.id);
				$uibModalInstance.close(Auth);
			},
			function(error){
				$scope.error = error.data.error;
			}
		);
	}
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
    }
}]);