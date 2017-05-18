"use strict";

angular.module("zerodha")
.controller("stockCtrl",
	["$scope", "stockService",
	function ($scope, stockService) {

		stockService.getData(function(response){
			$scope.topGainers = JSON.parse(response["topGainers"].replace(/'/g , "\""));
			$scope.topLosers = JSON.parse(response["topLosers"].replace(/'/g , "\""));
		});

		$scope.getRandomSpan = function(){
			return Math.floor((Math.random()*6)+1);
		}

		$(document).ready(function() {

			var username = 'zerodhaUrs'+$scope.getRandomSpan();
			var websocket = 'ws://0.0.0.0:3000/ws?username='+username;
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

				console.log("Socket Received")
				var data = JSON.parse(evt.data)
				$scope.topGainers = data.topGainers
				$scope.topLosers = data.topLosers
				$scope.$apply();
			};


		});

	}]);