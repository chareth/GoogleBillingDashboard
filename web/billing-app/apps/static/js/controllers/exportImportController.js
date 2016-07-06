/**
 * Created by ashwini on 3/23/16.
 */
var exportImportController = angular.module('exportImportController', []);
exportImportController
/**
 *  Main Page Projects Controller
 *  Gets the list of projects
 *  has modal setup for delete
 */
  .controller('exportController', ['$scope', '$log', '$rootScope',
    function ($scope, $log, $rootScope) {
      $scope.init = function () {
        $log.info(' --- EXPORT ---- CONTROLLER ----');
      };
      $scope.export = function (list, name) {
        var json = list;
        $scope.csv = $scope.JSON2CSV(json);
        var file_name = name + '.csv';
        //window.open("data:text/csv;charset=utf-8;filename=filename.csv," + escape(csv))
        $('a#export').attr('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent($scope.csv));
        $('a#export').attr('download', file_name);
        $('a.export').attr('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent($scope.csv));
        $('a.export').attr('download', file_name);
      };
      $scope.JSON2CSV = function (objArray) {
        var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;

        var str = '';
        var line = '';
        // get the header info, we need only month,cost,usage and not the angular stuff
        for (var index in array[0]) {
          if (index != '$$hashKey') {
            line += index + ',';
          }
        }
        line = line.slice(0, -1);
        str += line + '\r\n';


        for (var i = 0; i < array.length; i++) {
          var line = '';

          for (var index in array[i]) {
            if (index != '$$hashKey') {
              line += array[i][index] + ',';
            }

          }


          line = line.slice(0, -1);
          str += line + '\r\n';
        }
        return str;


      };


      $scope.init();


    }]);