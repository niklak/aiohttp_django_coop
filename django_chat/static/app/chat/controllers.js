angular.module('chat.controllers', ['chat.services', 'auth.services'])
.controller('ChannelListCtrl', [
    '$scope', '$rootScope', '$location' ,'$routeParams', 'Channel', 'Auth',
    function($scope, $rootScope, $location, $routeParams, Channel, Auth) {
        if (Auth.is_authenticated()){
            $scope.r = Channel.query();
        }
        else{
            $rootScope.alerts.push({ type: 'warning', msg: 'You need to log in to continue!' });
            $location.path('access_denied/');
        }
    }
])
.controller('ChannelCtrl', [
    '$scope', '$rootScope', '$location' ,'$routeParams', '$timeout', 'Channel', 'Message', 'Auth',
    function($scope, $rootScope, $location, $routeParams, $timeout, Channel, Message, Auth) {
        if (Auth.is_authenticated()){
            $scope.channel = Channel.get({pk: $routeParams.pk}, function(success){
                /*After you will implement your own pagination system, you have to add for
                $scope.messages some appropriate statements*/
                $scope.messages = Message.query({pk: $routeParams.pk});
                $scope.auth = Auth;
                $scope.sock = get_socket(success.id, Auth.token);

                $scope.$on("$routeChangeStart", function(event, next, current) {
                    $scope.sock.close();
                });

            });
            $timeout(function(){scroll_inbox_to_top()}, 1000);

        }
        else{
            $rootScope.alerts.push({ type: 'warning', msg: 'You need to log in to continue!' });
            $location.path('access_denied/');
        }

        function scroll_inbox_to_top(){
            var inbox = document.getElementById('inbox');
            inbox.scrollTop = inbox.scrollHeight;
        }

        function get_socket(channel_id, token) {
            var url = "ws://127.0.0.1:8080/chat/" + channel_id + '/' + token + '/';

            var sock = new WebSocket(url);
            sock.onmessage = function(event) {
                var message = JSON.parse(event.data);

                if (message.hasOwnProperty('user_list')){
                    $scope.users = message.user_list;
                }
                else if (message.hasOwnProperty('create_date')){
                    $scope.messages.push(message);
                }
                $scope.$apply();
                scroll_inbox_to_top();
            };
            sock.onclose = function(event){
                console.log(event); // delete in production
                $scope.users = ['Information unavailable'];
                $rootScope.alerts.push({ type: 'danger', msg: 'Server has closed the connection!' });
                $scope.$apply();
            };
            return sock;
        };



        $scope.send = function(){
            $scope.sock.send($scope.message);
            $scope.message = null;
        }
    }
])
.controller('CreateChannelCtrl', [
    '$scope', '$rootScope', '$location' , 'Channel', 'Message', 'Auth',
    function($scope, $rootScope, $location, Channel, Message, Auth) {
        if (!Auth.is_authenticated()){
            $rootScope.alerts.push({ type: 'warning', msg: 'You need to log in to continue!' });
            $location.path('access_denied/');
        }
        $scope.channel = {};
        $scope.create_channel = function(){
            $scope.channel.started_by = Auth.id;
            Channel.save($scope.channel, function(success){
                    $location.path('/');
                },
            function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: 'Error was happened!' });
                    $scope.error = error.data;
                }
            );
        };
    }
])
.controller('RegisterCtrl', ['$scope','$rootScope', '$location', 'RegUser', 'Auth',
    function($scope, $rootScope, $location, RegUser, Auth) {

        if (Auth.is_authenticated()){
            $location.path('/');
        }
        $scope.register = function() {
            $scope.user = RegUser.save($scope.reg,
                function(success){
                    $rootScope.alerts.push({ type: 'success',
                        msg: 'Your user account has been created. Now you can log in.' });
                    $location.path('/');
                },
                function(error){
                    $rootScope.alerts.push({ type: 'danger', msg: 'Error was happened!' });
                    $scope.error = error.data;
                }
            );
        };
    }
]);;