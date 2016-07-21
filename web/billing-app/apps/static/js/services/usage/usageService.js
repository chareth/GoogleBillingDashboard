var usageService = angular.module('usageService',[]);

usageService.factory('Usage', ['$http', '$log', '$timeout', '$q', '$httpParamSerializer', function($http, $log, $timeout, $q, $httpParamSerializer){

  var usages = {
    getUsageTable: function(year, month, project){
      var paramsObj = {'year':year, 'month':month, 'project':project};
      var paramStr = $httpParamSerializer(paramsObj);
      var url =CU.usage_url+"api/usagetable?";

      if (paramStr.length)  url +=paramStr + "&";

      url += "time_stamp=" +  Date.now();

      $log.info(url);
      var deferred = $q.defer();
      $http.get(url).success(function (data) {
        deferred.resolve(data);
      }).error(function () {
        deferred.reject("error");
      });
      return deferred.promise;
    },

    getProjectNames: function(){
      var deferred = $q.defer();
      var url = CU.usage_url + "api/projectnames?time_stamp=";
      url += Date.now();
      $log.info(url);
      $http.get(url).success(function(data){
        deferred.resolve(data);
      }).error(function(){
        deferred.reject("error");
      });
      return deferred.promise;
    }
  };

  return usages;

}]);
