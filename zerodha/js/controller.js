"use strict";
 
angular.module("zerodha", [
      'ngWebSocket' // you may also use 'angular-websocket' if you prefer
    ])
.factory('MyData', function($websocket) {

	console.log("factory")
      // Open a WebSocket connection
      var ws = new WebSocket("ws://localhost:8000/socket/");
    
	    ws.onopen = function(){  
	        console.log("Socket has been opened!");  
	    };
	    
	    ws.onmessage = function(message) {
	        listener(JSON.parse(message.data));
	    };


      return methods;
    }) 
.controller("stockCtrl",
  ["$scope", "stockService",
  function ($scope, stockService) {
      console.log("hello")
      stockService.getData(function(response){
      	$scope.topGainers = JSON.parse(response["topGainers"].replace(/'/g , "\""));
      	$scope.topLosers = JSON.parse(response["topLosers"].replace(/'/g , "\""));
      	console.log($scope.topGainers)
      	console.log($scope.topLosers)
      });

      $scope.getRandomSpan = function(){
  			return Math.floor((Math.random()*6)+1);
		}
      $(document).ready(function() {

      		var username = 'zerodhaUrs'+$scope.getRandomSpan();
          var websocket = 'ws://54.254.133.3:3000/ws?username='+username;
          var ws ;
          if (window.WebSocket) {
            ws = new WebSocket(websocket, ['zerodha']);
          }
          else if (window.MozWebSocket) {
            ws = MozWebSocket(websocket);
          }
          else {
            console.log('WebSocket Not Supported');
            return;
          }

          
          ws.onmessage = function (evt) {
          	var data = JSON.parse(evt.data)
          	$scope.topGainers = data.topGainers
          	$scope.topLosers = data.topLosers
             console.log($scope.topGainers)
          };
          ws.onopen = function() {
             ws.send( username + " entered the room");
          };
          
        });
  
}]);