var navbar = angular.module('navbar', ['auth.services'])
.directive('dNavbar', ['Login', 'Logout', 'Auth', '$uibModal', '$window', 'aCartHandler','PATH',
						function(Login, Logout, Auth, $uibModal, $window, aCartHandler, PATH) {
	return {
		restrict: 'A',
		templateUrl: PATH + 'partials/navbar/navbar.html',
		controller: function($scope, $rootScope, Logout, Auth, $uibModal, $window, aCartHandler, PATH){

			angular.element($window).bind('scroll', function() {
				$scope.change_class = (this.pageYOffset >= 100) ? true : false;
				$scope.$apply();
			});
			$scope.brand_text = 'Example chat';
			/* Linking */
			$scope.auth = Auth;
			set_links();
			function set_links (){
				$scope.profile_link = '#!/profile/' + $scope.auth.id;
	            $scope.link = $scope.profile_link + '/change_password/';
			}

			$scope.selected = null;
			$scope.select = function (index) { $scope.selected = index; };
			$scope.logout = function(){
				$scope.r = Logout.query(function(r){
				    $rootScope.alerts.push({ type: 'info', msg: 'Пока, ' + Auth.username + '.'});
					$scope.auth.remove();
					aCartHandler.refresh();
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
					set_links();
					aCartHandler.refresh();
				});
			};

			$scope.toggleAnimation = function () {
				$scope.animationsEnabled = !$scope.animationsEnabled;
			};
		}
	};
}]);

navbar.controller('ModalInstanceCtrl', ['$scope', '$uibModalInstance' , 'Login', 'Auth',
										function ($scope, $uibModalInstance, Login, Auth) {

	$scope.authenticate = function(u, p){
		$scope.r = Login.query({username: u, password: p },
			function(success){
				$scope.error = null;
				Auth.set(success.id, success.username);
				$uibModalInstance.close(Auth);
			},
			function(error){
				$scope.error = error.data.error;
			}
		);
	}
	$scope.cancel = function () {
		$uibModalInstance.dismiss('отмена');
    }
}]);