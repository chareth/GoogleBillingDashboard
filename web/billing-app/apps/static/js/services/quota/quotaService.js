/**
 * Created by ashwini on 3/9/16.
 */

'use strict';

/* Services */

var quotaService = angular.module('quotaService', []);


quotaService.factory('Quota', ['$http', '$timeout', '$q', '$log' , function ($http, $timeout, $q, $log) {
    var quotas = {
        baseUrl: '',
        getCPUList: function () {
            var url = CU.quota_url + '?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            $log.info(url);
            $http.get(url).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        }};
    return quotas;
}]);