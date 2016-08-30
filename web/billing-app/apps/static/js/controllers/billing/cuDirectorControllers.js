'use strict';

/* Controllers */

var cuDirectorsControllers = angular.module('cuDirectorsControllers', []);


/*
 * Controller for Billing per Cost Center View page
 * */
cuDirectorsControllers.controller('DirectorController', ['$scope', '$location' , '$cookies',
  'UsageCost', '$log', '$sce', '$filter',
  function ($scope, $location, $cookies, UsageCost, $log, $sce, $filter) {
    var init = function () {
      $scope.costCenterList = [];
      $scope.fail = false;
      $scope.loading = true;
      $scope.totalCost = 0;
      $scope.totalDirectorCost = 0;
      $scope.totalPercent = 0;
      $scope.supportTotal = 0;
      $scope.totalToPay = 0;

      var currentDate = new Date();
      $scope.currentFullYear = currentDate.getFullYear();
      $scope.currentYear = currentDate.getFullYear().toString().substr(2, 2);
      $scope.currentMonth = currentDate.getMonth() + 1;


      $scope.current_month = $scope.currentYear + '-' + $scope.currentMonth;
      $scope.monthSelected = $scope.current_month;

      $scope.getCostCenterList($scope.current_month);
    };

    $scope.isSupport = function (cost_center) {
      if (cost_center.id == 'support') {
        return true;
      }
      else {
        return false;
      }
    };
    /**
     *
     * @param year_month
     * once the costcenter list is there
     *  -- calculate the overall cost
     *  -- calculate the support cost
     *  -- calculate the cost without support
     *    -- this is used to calculate the support cost each director should pay
     *  -- once all %usage and support cost per director is calculated remove the support cost from the list
     */

    $scope.getCostCenterList = function (year_month) {
      $scope.loading = true;
      UsageCost.getData('month', year_month, 'month', 'all', 'all', 'all').then(function (value) {
        $scope.loading = false;
        $scope.costCenterList = value.usage_data;
        $scope.totalCost = 0;
        $scope.totalDirectorCost = 0;
        $scope.totalPercent = 0;
        $scope.supportTotal = 0;
        $scope.totalToPay = 0;
        $.each($scope.costCenterList, function (k, v) {
          $scope.totalCost += v.cost;
          v.directorName = v.name;
          if (v.id == 'support') {
            $scope.supportCost = v.cost;
          }
        });
        $scope.totalCostWithoutSupport = $scope.totalCost - $scope.supportCost;

        $.each($scope.costCenterList, function (k, v) {
          v.percentUsed = (v.cost * 100) / ($scope.totalCostWithoutSupport);
          v.supportUsed = (v.percentUsed * $scope.supportCost) / 100;
          v.total = v.supportUsed + v.cost;
          if (v.id != 'support') {
            $scope.totalDirectorCost += v.cost;
            $scope.totalPercent += v.percentUsed;
            $scope.supportTotal += v.supportUsed;
            $scope.totalToPay += v.total;
          }


        });
        $.each($scope.costCenterList, function (k, v) {
          if (v.id == 'support') {
            $scope.costCenterList.splice(k, 1);
            return false;
          }

        });

        $log.info($scope.costCenterList);


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
      var url = 'cost_center/#?' + '&span=month&span_value=' + $scope.monthSelected + '&view_by=month&cost_center=' + center + '&project=all' + '&resource=all';
      return url;
    };

    $scope.getBillingData = function () {

      if ($scope.dt != null) {
        $scope.costCenterList = [];
        $scope.loading = true;
        $scope.totalCost = 0;
        var year_month = $scope.dt.getFullYear().toString().substr(2, 2) + '-' + ($scope.dt.getMonth() + 1);
        $scope.monthSelected = year_month;
        $log.info(year_month);
        $scope.getCostCenterList(year_month);
      }


    };

    /**
     * Date Picker
     */
    $scope.datePicker = function () {
      $scope.dt = new Date();
      $scope.clear = function () {
        $scope.dt = null;
      };
      $scope.dateOptions = {
        'year-format': "'yy'",
        'starting-day': 1,
        'datepicker-mode': "'month'",
        'min-mode': "month"
      };


      // Disable weekend selection
      function disabled(data) {
        var date = data.date,
          mode = data.mode;
        return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
      }

      $scope.open1 = function () {
        $scope.popup1.opened = true;
      };

      $scope.open2 = function () {
        $scope.popup2.opened = true;
      };


      $scope.popup1 = {
        opened: false
      };

      $scope.popup2 = {
        opened: false
      };
    };


    $scope.datePicker();

    init();

  }]);

