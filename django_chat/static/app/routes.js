angular.module('routes', [
    'ngRoute',
    'chat.controllers',
])
.config(['$routeProvider','PATH',
    function($routeProvider, PATH) {
        $routeProvider.
        when('/', {
            templateUrl: PATH + 'chat/templates/channel_list.html',
            controller: 'ChannelListCtrl'}).
        when('/channels/new/', {
            templateUrl: PATH + 'chat/templates/create_channel.html',
            controller: 'CreateChannelCtrl'}).
        when('/channels/:pk/', {
            templateUrl: PATH + 'chat/templates/channel.html',
            controller: 'ChannelCtrl'}).
        when('/register/', {
            templateUrl: PATH + 'chat/templates/register.html',
            controller: 'RegisterCtrl'}).
        when('/404/', {
            templateUrl: PATH + 'partials/error/404.html'}).
        when('/access_denied/', {
            templateUrl: PATH + 'chat/templates/access_denied.html'}).
        when('/logout/', {
            templateUrl: PATH + 'chat/templates/logout.html'}).
        otherwise({redirectTo: '/error/404/',});
    }
]);
