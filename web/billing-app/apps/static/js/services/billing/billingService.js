'use strict';

/* Services */

var billingService = angular.module('billingService', []);
/* Usage Cost Services*/

billingService.factory('UsageCost', ['$http', '$timeout', '$q', '$log' , function ($http, $timeout, $q, $log) {
    var usages = {
        baseUrl: '',
        getProjectList: function () {
            var url = CU.billing_url + 'projects?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            $log.info(url);
            $http.get(url).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        getResourceList: function () {
            var url = CU.billing_url + 'resources?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            $log.info(url);
            $http.get(url).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        getUrl: function (spanSelected, spanValueSelected, viewSelected, costCenterSelected, projectSelected, resourceSelected) {
            var url = CU.billing_url, span, span_value, view_by, project, resource, cost_center,year;

            if(spanSelected =='year'){
                year = spanValueSelected;
            }else if(spanSelected =='month' || spanSelected =='quarter'){
                year = 20 +spanValueSelected.split('-')[0];
            }else if(spanSelected =='week'){

               year =  spanValueSelected.split('-')[2]
            }
            span = '&span=' + spanSelected;
            span_value = '&span_value=' + spanValueSelected;
            view_by = '&view_by=' + viewSelected;
            cost_center = '&cost_center=' + costCenterSelected;
            project = '&project=' + projectSelected;
            resource = '&resource=' + resourceSelected;


            url = url + year + '?' + span + span_value + view_by;
            url = url + cost_center + project + resource + '&time_stamp=' + Date.now();
            return url;
        },
        getData: function (spanSelected, spanValueSelected, viewSelected, costCenterSelected, projectSelected, resourceSelected) {
            var billing_url = usages.getUrl(spanSelected, spanValueSelected, viewSelected, costCenterSelected, projectSelected, resourceSelected),
                deferred = $q.defer();
            $log.info(billing_url);
            $http.get(encodeURI(billing_url)).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        getCostCenterList: function (unique) {
            var url = CU.billing_url + 'cost_center?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            if (unique) {
                url += '&unique=true';
            }
            $log.info(url);
            $http.get(encodeURI(url)).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        deleteProject: function (project) {
            var url = CU.billing_url + 'cost_center/delete?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            $log.info(url);
            $http.post(encodeURI(url), project).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        addProject: function (project) {
            var url = CU.billing_url + 'cost_center?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            $log.info(url);
            $http.post(encodeURI(url), project).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        }
    };
    return usages;
}]);