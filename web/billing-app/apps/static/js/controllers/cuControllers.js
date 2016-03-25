'use strict';
var cuControllers = angular.module('cuControllers', [
  'cuLoginController'
]);


/*
 * Controller for tadding active class to the menu*/
cuControllers.controller('menuBar', ['$scope', '$location' , '$modal', '$cookies', 'Login', '$log', '$routeParams',
  function ($scope, $location, $modal, $cookies, Login, $log, $routeParams) {
    $scope.isActive = function (viewLocation) {
      if ($scope.active == viewLocation.split('/')[1]) {
        return true;
      }


    };
    $scope.modal = function () {
      $modal.open({
        templateUrl: '/static/partials/login.html',
        controller: 'LoginController',
        size: 'sm',
        backdrop: 'static'
      });

    };

    $scope.logout = function () {
      Login.logout($cookies.get('cloudUser')).then(function (value) {
        $scope.login_cookie = '';
        $cookies.remove('cloudAdminCookie', {path: '/'});
        $cookies.remove('cloudUser', {path: '/'});
        $cookies.put('cloudAdminCookie', '', {path: '/'});
        $cookies.put('cloudUser', '', {path: '/'});
        $scope.user = '';
        window.location.reload();
        $log.info('Logout Complete');
      }, function (reason) {

        $log.error('Reason for Failure ---', reason);
      }, function (update) {
        $log.info('Update  ---', update);
      });

    }

  }]);
/*
 * Controller for tadding active class to the menu*/
cuControllers.controller('exportData', ['$scope', '$location' , '$log',
  function ($scope, $location, $log) {
    $scope.export = function (data, name) {
      var json = data;
      var csv = $scope.JSON2CSV(json);
      //window.open("data:text/csv;charset=utf-8;filename=filename.csv," + escape(csv))
      $('a#export').attr('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
      $('a#export').attr('download', name);
    };
    $scope.JSON2CSV = function (objArray) {
      var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;

      var str = '';
      var line = '';
      // get the header info, we need only month,cost,usage and not the angular stuff
      for (var index in array[0]) {
        line += index.toUpperCase() + ',';
      }
      line = line.slice(0, -1);
      str += line + '\r\n';


      for (var i = 0; i < array.length; i++) {
        var line = '';

        for (var index in array[i]) {
          line += array[i][index] + ',';
        }


        line = line.slice(0, -1);
        str += line + '\r\n';
      }
      return str;


    };

  }]);