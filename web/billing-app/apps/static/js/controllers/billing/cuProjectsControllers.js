'use strict';

/* Controllers */

var cuProjectsControllers = angular.module('cuProjectsControllers', []);


/*
 * Controller for Billing per Cost Center View page
 * */
cuProjectsControllers.controller('CostCenterController', ['$scope', '$location' , '$cookies',
  'UsageCost', '$log', '$sce',
  function ($scope, $location, $cookies, UsageCost, $log, $sce) {
    var init = function () {
      $scope.costCenterList = [];
      $scope.fail = false;
      $scope.loading = true;
      $scope.totalCost = 0;
      $scope.getCostCenterList();
    };
    $scope.getCostCenterList = function () {
      var currentDate = new Date();
      $scope.currentFullYear = currentDate.getFullYear();
      $scope.currentYear = currentDate.getFullYear().toString().substr(2, 2);
      $scope.currentMonth = currentDate.getMonth() + 1;


      $scope.current_month = $scope.currentYear + '-' + $scope.currentMonth;

      UsageCost.getData('month', $scope.current_month, 'month', 'all', 'all', 'all').then(function (value) {
        $scope.loading = false;
        $scope.costCenterList = value.usage_data;
        $scope.totalCost = 0;
        $.each(value.usage_data, function (k, v) {
          $scope.totalCost += v.cost;
        });
        $log.info('Cost Center Data -- ', $scope.costCenterList);
      }, function (reason) {
        var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
        $log.error('Reason for Failure ---', msg);
        $scope.fail = true;
        $scope.class_name = 'red';
        $scope.loading = false;
        $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);

      }, function (update) {
        $log.info('Update  ---', update);
      });

    };

    $scope.centerURL = function (center) {
      var url = 'cost_center/#?' + '&span=year&span_value=' + $scope.currentFullYear + '&view_by=month&cost_center=' + center + '&project=all' + '&resource=all';
      return url;
    };

    $scope.getMonthlyProjectBillingPerCenter = UsageCost.getMonthlyProjectBillingPerCenter;

    init();

  }]);


/*
 * Controller for Cost Center View page*/
cuProjectsControllers.controller('ProjectsController', ['$scope', '$location' , '$uibModal', '$cookies',
  'UsageCost', '$log', '$sce',
  function ($scope, $location, $uibModal, $cookies, UsageCost, $log, $sce) {
    var init = function () {

      $scope.getCostCenterList();
      $scope.projectList = [];
      $scope.message = false;
      $scope.add = false;
      $scope.project_id = '';
      $scope.project_name = '';
      $scope.cost_center = '';
      $scope.director = '';

    };
    $scope.getCostCenterList = function () {
      UsageCost.getCostCenterList().then(function (value) {

        $log.info(value);
        $scope.projectList = value.cost_center_list;
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

    $scope.addOne = function (project) {
      $scope.add = true;


      if (project) {
        $scope.projectInfo = angular.copy(project);
        $scope.projectInfo.project_id = ($scope.projectInfo.project_id).indexOf('ID') == 0 ? $scope.getProjectId($scope.projectInfo.project_id) : $scope.projectInfo.project_id;
        $scope.add_project = false;

      } else {
        $scope.projectInfo = {'project_id': '', 'project_name': '', 'director': '', 'cost_center': '', 'director_email': '', 'contact_name': '', 'contact_email': '', 'alert_amount': '', 'monthly_budget': ''};
        $scope.add_project = true;
      }

      $log.info($scope.projectInfo);

      $log.debug(project);
      $('html, body').animate({
        scrollTop: 0
      }, 800);

    };
    $scope.close_add = function () {
      $scope.add = false;
      $scope.loading = false;
      $log.debug('Close --', $scope.projectInfo);

      $scope.projectInfo = {'project_id': '',
        'project_name': '', 'director': '',
        'cost_center': '', 'director_email': '',
        'contact_name': '', 'contact_email': '',
        'alert_amount': ''};
    };
    $scope.add_save = function () {
      $log.info($scope.projectInfo);
      if ($scope.projectInfo.project_id != 'Not Available') {
        $scope.projectInfo.project_id = 'ID-' + $scope.projectInfo.project_id;
      }
      var project = {'projects': [$scope.projectInfo]};
      var id = $scope.projectInfo.project_name;

      var container = $('table thead'),
        element = $("tr#" + id + "");
      $scope.loading = true;

      UsageCost.addProject(project).then(function (value) {

        $log.info(value);
        $scope.getCostCenterList();
        $scope.close_add();
        $('html, body').animate({
          scrollTop: element.offset().top - container.offset().top + container.scrollTop()
        });
        element.addClass

      }, function (reason) {
        var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
        $log.error('Reason for Failure ---', msg);
        $scope.fail = true;
        $scope.class_name = 'red';
        $('#container').html('');
        $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);
        $scope.close_add();
      }, function (update) {
        $log.info('Update  ---', update);
      });

    };
    $scope.clear = function () {
      $scope.message = false;
    };

    $scope.delete = function (project) {
      $scope.showModal('delete', project);
    };
    $scope.showModal = function (type, project) {

      $uibModal.open({
        templateUrl: '/static/partials/billing/projectInfo.html',
        controller: 'ProjectInfoController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          project: function () {
            return project;
          },
          type: function () {
            return type;
          }

        }});

    };

    $scope.$on("getCostCenterList", function (event, args) {

      $scope.getCostCenterList();

    });
    /**
     * split the id to not to display the ID in the UI
     * @param projectID
     */
    $scope.getProjectId = function (projectID) {
      var new_id;
      new_id = projectID.substr(projectID.indexOf("-") + 1);
      return new_id;
    };
    init();

  }]);


/**
 * Project Delete  Modal Controller
 */
cuProjectsControllers.controller('ProjectInfoController', ['$scope', '$uibModalInstance' , 'project', '$log', 'type', '$rootScope',
  'UsageCost', '$sce',
  function ($scope, $uibModalInstance, project, $log, type, $rootScope, UsageCost, $sce) {
    $scope.fail = false;
    $scope.project = project;
    $scope.type = type;


    $scope.close = function () {
      $uibModalInstance.dismiss('cancel');

    };
    $scope.delete = function () {
      var project = {'projects': [$scope.project.project_id]};
      $scope.loading = true;

      UsageCost.deleteProject(project).then(function (value) {
        $log.info(value);
        $scope.loading = false;
        $uibModalInstance.dismiss('cancel');
        $rootScope.$broadcast('getCostCenterList');
      }, function (reason) {
        var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
        $log.error('Reason for Failure ---', msg);
        $scope.fail = true;
        $scope.loading = false;
        $scope.class_name = 'red';
        $('#container').html('');
        $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);
        $rootScope.$broadcast('getCostCenterList', {'message': $scope.message});

      }, function (update) {
        $log.info('Update  ---', update);
      });

    };

  }]);
