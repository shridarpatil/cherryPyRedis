'use strict';

angular.module('zerodha')

.factory('stockService',
  ['$http', '$timeout',
  function ($http,  $timeout) {
    var service = {};

    service.getData = function (callback) {

      $http.get('http://0.0.0.0:3000/displayData')
      .success(function (response) {
        callback(response);
      })
      .error(function(response){
        console.log(response)
      });

    };
    return service;
  }]);

