var app = angular.module('main', [
    'constants',
    'routes',
    'ui.bootstrap',
    'navbar',
    'alert',
    ]);
app.factory('httpRequestInterceptor', function () {
    return {
        request: function (config) {
            config.headers["X-Requested-With"] = "XMLHttpRequest";
            return config;
        }
    };
});
app.config(function ($httpProvider) {
    $httpProvider.interceptors.push('httpRequestInterceptor');
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.useApplyAsync(true);
});
app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});
app.config(['$locationProvider', function($locationProvider){
    $locationProvider.hashPrefix('!');
}]);