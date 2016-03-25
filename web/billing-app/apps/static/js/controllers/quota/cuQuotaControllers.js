/**
 * Created by ashwini on 3/9/16.
 */
'use strict';

/* Controllers */

var cuQuotaControllers = angular.module('cuQuotaControllers', []);

cuQuotaControllers.controller('CPUQuotaListController', ['$scope', '$log', '$sce', 'Quota', '$location', 'UsageCost',
  function ($scope, $log, $sce, Quota, $location, UsageCost) {

    var init = function init() {
      $log.info('----- CPU Controller INIT --- ');

      $scope.centerSelected = 'all';
      $scope.regionSelected = '';
      $scope.metricSelected = '';
      $scope.projectSelected = 'one';

      $scope.costCenterList = [];
      $scope.projectList = [];
      $scope.regionsList = [];
      $scope.metricsList = [];
      $scope.regionList = [];
      // get the url params
      $scope.getURLParams();
    };

    /**
     * get the url params to match the filter
     */
    $scope.getURLParams = function getURLParams() {
      var params = $location.search();
      //if params not found then first time get the center list and set it to one
      if (!params.cost_center) {
        $scope.centerSelected = 'all';
        $scope.projectSelected = 'one';
        $location.search('cost_center', $scope.centerSelected);
        $location.search('project', null);
      } else if (!params.project) {
        $scope.projectSelected = 'one';
        $scope.centerSelected = params.cost_center;
      } else {
        $scope.centerSelected = params.cost_center;
        $scope.projectSelected = params.project;
      }
      getCostCenterList();
    };
    /* on location change call filter change with the updated params
     * */
    $scope.$on('$locationChangeSuccess', function (next, current) {
      $log.info('Location Change Called');
      var params = $location.search();
      if (params.cost_center && !params.project) {
        $scope.centerSelected = params.cost_center;
        $scope.setDefaults('one');
        if ($scope.costCenterList.length == 0) {
          getCostCenterList();
        } else if ($scope.projectList.length == 0) {
          $scope.getProjectList();
        }
      } else if (params.cost_center && params.project != 'one') {
        $scope.centerSelected = params.cost_center;
        $scope.projectSelected = params.project;
        $scope.getCPUQuota();
      }
    });

    $scope.updateURLParams = function updateURLParams(center, project) {

      if (!project || project == 'one') {
        $location.search('cost_center', center);
        $location.search('project', null);
        $scope.projectSelected = 'one';
        $scope.fail = false;
        //$scope.getProjectList();
      } else {
        $location.search('cost_center', center);
        $location.search('project', project);
        //$scope.getCPUQuota();
      }

    };
    $scope.setDefaults = function setDefaults(project) {
      if (project == 'one') {
        $scope.projectList = [];
        $scope.regionsList = [];
        $scope.metricsList = [];
        $scope.regionList = [];
      } else {
        $scope.projectSelected = project;
        $scope.regionsList = [];
        $scope.metricsList = [];
        $scope.regionList = [];
        $scope.loading = true;
        $scope.fail = false;

      }
    };
    var getCostCenterList = function getCostCenterList() {
      UsageCost.getCostCenterList(true).then(function (value) {

        $log.info(value);
        $scope.costCenterList = value.cost_center_list;
        $scope.setDefaults($scope.projectSelected);
        $scope.getProjectList();

      }, function (reason) {
        var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
        $log.error('Reason for Failure ---', msg);
        $scope.fail = true;
        $scope.class_name = 'red';
        $('#container').html('');
        $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);

      }, function (update) {
        $log.info('Update  ---', update);
      });

    };
    /**
     *
     * @param center
     * @returns {boolean}
     * based on the center value get the list of projects and update the url as well
     */

    $scope.getProjectList = function getProjectList() {
      $scope.projectList = [];
      $scope.loading = true;
      $scope.setDefaults($scope.projectSelected);
      UsageCost.getProjectList($scope.centerSelected).then(function (value) {
        $log.info(value);
        $scope.loading = false;
        $scope.projectList = value;
        if ($scope.projectSelected != 'one') {
          $scope.getCPUQuota();
        }

      }, function (reason) {
        var msg = (reason.data && reason.data.message) ? reason.data.message : CU.error_msg;
        $log.error('Reason for Failure ---', msg);
        $scope.fail = true;
        $scope.loading = false;
        $scope.class_name = 'red';
        $('#container').html('');
        $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);

      }, function (update) {
        $log.info('Update  ---', update);
      });
    };
    /**
     * get the CPU data based on the project selected
     */

    $scope.getCPUQuota = function getCPUQuota() {
      $scope.setDefaults($scope.projectSelected);

      UsageCost.getQuota($scope.projectSelected).then(function (value) {
        $scope.loading = false;
        $scope.regionsList = value;
        $scope.getUniqueLists();
      }, function (reason) {
        var msg = (reason.data && reason.data.message) ? reason.data.message : CU.error_msg;
        $log.error('Reason for Failure ---', msg);
        $scope.fail = true;
        $scope.loading = false;
        $scope.class_name = 'red';
        $('#container').html('');
        $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);

      }, function (update) {
        $log.info('Update  ---', update);
      });
    };

    /**
     * get unique region list and metrics list
     */
    $scope.getUniqueLists = function getUniqueLists() {

      angular.forEach($scope.regionsList, function (key, val) {
        $scope.regionList.push(key['name']);
        angular.forEach(key['quotas'], function (k, value) {
          if ($scope.metricsList.indexOf(k['metric']) == -1) {
            $scope.metricsList.push(k['metric']);
          }
        });
      });
    };
    /**
     * add class basedon status
     */
    $scope.regionStatus = function regionStatus(status) {
      if (status == 'UP') {
        return 'fa fa-arrow-up text-success';
      } else if (status == 'DOWN') {
        return 'fa fa-arrow-up text-danger';
      }
    };
    /**
     * get usage %
     */
    $scope.getUsage = function getUsage(usage, limit, metric) {
      metric.usage_percent = parseFloat(((usage / limit) * 100).toFixed(2));
      metric.width = metric.usage_percent + '%';
      if (metric.usage_percent <= 50) {
        return 'progress-bar progress-bar-success';

      } else if (metric.usage_percent > 51 && metric.usage_percent <= 70) {
        return 'progress-bar progress-bar-warning';

      } else if (metric.usage_percent > 71) {
        return 'progress-bar progress-bar-danger';
      }

    };
    /**
     * get export data
     */



    init();
  }
])
;
