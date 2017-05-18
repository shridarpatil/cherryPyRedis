'use strict';
 
angular.module('zerodha')
 
.factory('stockService',
    ['$http', '$timeout',
    function ($http,  $timeout) {
        var service = {};
        
        service.getData = function (callback) {

            $http.get('http://54.254.133.3:3000/displayData')
               .success(function (response) {
                    console.log("service")
                   callback(response);
               })
               .error(function(response){
                console.log(response)
               });

        };
 
       

        
 
        return service;
    }])
 
