var usageController = angular.module('usageController', []);

usageController.controller('usageController', ['$scope',  '$log', '$sce', 'Usage', function($scope, $log, $sce, Usage){

  $scope.usageTable = [];

  // lists used for dropdowns
  $scope.yearsList = [];
  $scope.monthsList = [];
  $scope.projectsList = [];

  // query string values
  $scope.year;
  $scope.month;
  $scope.project;

  $scope.sortType;
  $scope.sortReverse;

  $scope.loading;
  $scope.fail;


  $scope.init = function(){
    console.log("---- init called");
    $scope.monthsList = [
        {'month':'January', 'num':1},   {'month':'February', 'num':2},
        {'month':'March', 'num':3},     {'month':'April', 'num':4},
        {'month':'May', 'num':5},       {'month':'June', 'num':6},
        {'month':'July', 'num':7},      {'month':'August', 'num':8},
        {'month':'September', 'num':9}, {'month':'October', 'num':10},
        {'month':'November', 'num':11}, {'month':'December', 'num':12}
      ];

    var date = new Date();
    var yr = date.getFullYear();
    $scope.yearsList.push(yr);
    $scope.yearsList.push(yr-1);

    $scope.year = null;
    $scope.month= null;
    $scope.project = null;

    $scope.sortType = "usage_date";
    $scope.sortReverse = false;

    $scope.loading = true;
    $scope.fail = false;

    setTimeout(function () {
      $scope.getProjectNames();
      $scope.getUsageTable();

    }, 1000);

  };

  $scope.getUsageTable = function(){
    $scope.loading = true;
    Usage.getUsageTable($scope.year, $scope.month, $scope.project).then(function(value){
      $scope.usageTable = value;
      $scope.loading = false;
    },function (reason) {
      var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
      $log.error('Reason for Failure ---', msg);
      $scope.fail = true;
      $scope.class_name = 'red';
      $scope.loading = false;
      $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);
    }, function(update){
      $scope.loading = false;
      $log.info('Update ---', update);
    });
  };

  $scope.getProjectNames = function(){
    Usage.getProjectNames().then(function(value){
      $scope.projectsList = value;
    }, function(update){
      $log.info('Update ---', update);
    });
  };

  // clear filters
  $scope.reset = function (){
    $scope.year = null;
    $scope.month= null;
    $scope.project = null;
    $scope.getUsageTable();

  };

  $scope.init();

}]);
