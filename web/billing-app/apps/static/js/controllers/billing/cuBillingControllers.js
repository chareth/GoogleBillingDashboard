'use strict';

/* Controllers */

var cuBillingControllers = angular.module('cuBillingControllers', []);

/*
 * controller for getting the usage nad billing data and display it as a chart
 * Dependencies -- $log, UsageServices
 * variables -- list for year, month, project and resource
 *
 * functions -- getYearList  --> liet of years
 *              getProjectList  --> list of projects -- name
 *              getResourceList  --> list of resources
 *              getURLparams --> to get the url params and set the filters and data accordingly
 *              updateURL -->     Called to update the url params based on the filter change and on initial page load
 *              filterChange --> based on the dropdwon change this will be called when updateURL is triggered
 *              getData  --> calls the Service to get the data from backend
 *              barChart  --> bar chart is displayed for cost
 *              multiChart --> cost nad usage
 *              monthName  --> for table get the
 *              projectURL -- create urls for the project
 *              export --> export toexcel
 *
 *
 * */
cuBillingControllers.controller('UsageController', ['$scope', '$log', '$sce', 'UsageCost', '$location',
    function ($scope, $log, $sce, UsageCost, $location) {
        $log.info(' ~~~~~~~~~~~~~UsageController Loaded ~~~~~~~~~~~~');
        $scope.init = function () {
            $scope.fail = false;
            $scope.totalCost = 0;


            /*get the current/last values*/
            var currentDate = new Date();
            $scope.currentFullYear = currentDate.getFullYear();
            $scope.currentYear = currentDate.getFullYear().toString().substr(2, 2);
            $scope.lastFullYear = $scope.currentFullYear - 1;
            $scope.lastYear = ($scope.currentFullYear - 1).toString().substr(2, 2);
            $scope.currentMonth = currentDate.getMonth() + 1;
            $scope.currentWeek = currentDate.getWeek();
            $scope.currentQuarter = parseInt(currentDate.getMonth() / 3) + 1;


            /* Main Span Drop Down*/
            $scope.spanList = {
                'year': 'Year',
                'quarter': 'Quarter',
                'month': 'Month',
                'week': 'Week'
            };
            /* Span value LIst creation*/
            /* last 2 years*/
            $scope.yearList = {};
            $scope.yearList[$scope.currentFullYear] = $scope.currentFullYear;
            $scope.yearList[$scope.lastFullYear] = $scope.lastFullYear;

            /* last 2 years 8 quarters*/

            $scope.quarterList = {};
            var quarter = ['q1', 'q2', 'q3', 'q4'];
            $.each(quarter, function (key, value) {
                var text = $scope.currentYear + '-' + value;
                var id = $scope.currentYear + '-' + (key + 1);
                $scope.quarterList[id] = text;
                text = $scope.lastYear + '-' + value;
                id = $scope.lastYear + '-' + (key + 1);
                $scope.quarterList[id] = text;

            });

            /* last 2 years month list*/
            $scope.monthList = {};
            $scope.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

            $.each($scope.months, function (key, value) {
                if ($scope.currentMonth >= key) {
                    var text = $scope.currentYear + '-' + value;
                    var id = $scope.currentYear + '-' + (key + 1);
                    $scope.monthList[id] = text;
                }
                text = $scope.lastYear + '-' + value;
                id = $scope.lastYear + '-' + (key + 1);
                $scope.monthList[id] = text;
            });
            $scope.weekList = {};


            getWeeks($scope.lastFullYear, 1);
            getWeeks($scope.currentFullYear, 1);


            $scope.dayList = {
                '60': 'Last 60 Days',
                '30': 'Last 30 Days'
            };

            $scope.spanValue = {
                'year': $scope.yearList,
                'quarter': $scope.quarterList,
                'month': $scope.monthList,
                'week': $scope.weekList,
                'day': $scope.dayList
            };
            $scope.viewValue = {
                'year': {
                    //  'year': 'Year',
                    'quarter': 'Quarter',
                    'month': 'Month',
                    'week': 'Week',
                    'day': 'Days'
                },
                'quarter': {
                    //'year': 'Year',
                    //'quarter': 'Quarter',
                    'month': 'Month',
                    'week': 'Week',
                    'day': 'Days'
                },
                'month': {
                    //'year': 'Year',
                    'month': 'Month',
                    'week': 'Week',
                    'day': 'Days'
                },
                'week': {
                    //'year': 'Year',
                    'week': 'Week',
                    'day': 'Days'
                },
                'day': {
                    'day': 'Days'
                }
            };

            /* by default selected values for the span
             * Changed based on the dropdown selected or url change or click*/
            $scope.yearSelected = $scope.currentFullYear;
            $scope.quarterSelected = $scope.currentQuarter;
            $scope.monthSelected = $scope.currentMonth;
            $scope.weekSelected = $scope.currentWeek;
            $scope.daySelected = 60;
            $scope.viewSelected = 'month';
            $scope.projectSelected = 'all';
            $scope.costCenterSelected = 'all';
            $scope.resourceSelected = 'all';
            $scope.spanSelected = 'year';
            $scope.spanValueSelected = 'year';

            $scope.spanValueList = $scope.spanValue[$scope.spanSelected];
            $scope.viewList = $scope.viewValue[$scope.spanSelected];

            $scope.display_table = false;
            //$('select').attr('disabled', true);
            $('#d3-container').html('<div class="text-center panel-body">' + CU.Loading + '</div>');

            /* get the start values based on the url params*/
            getURLParams();


        };


        /*  Based on the url params call update params and call filterchange  function that calls to get the data
         * */
        var getURLParams = function () {
            $scope.urlParams = $location.search();
            if ($scope.urlParams['span']) {
                $.each($scope.urlParams, function (k, v) {
                    if (k == 'span') {
                        $scope.spanSelected = v;
                    } else if (k == 'span_value') {
                        $scope.spanValueSelected = v;
                    } else if (k == 'view_by') {
                        $scope.viewSelected = v;
                    } else if (k == 'cost_center') {
                        $scope.costCenterSelected = v;
                    } else if (k == 'project') {
                        $scope.projectSelected = v;
                    } else if (k == 'resource') {
                        $scope.resourceSelected = v;
                    }
                });
            } else {
                /* first time while coming form home page*/
                $scope.spanSelected = 'year';
                $scope.spanValueSelected = 'year';
                $scope.viewSelected = 'month';
                $scope.costCenterSelected = 'all';
                $scope.projectSelected = 'all';
                $scope.resourceSelected = 'all';
            }
            $scope.updateURL();

            /* by default show data for current month and year*/
            $log.info('getURLParams');
            $log.info('$scope.spanSelected, $scope.spanValueSelected, $scope.viewSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected');
            $log.info($scope.spanSelected, $scope.spanValueSelected, $scope.viewSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);

            $scope.filterChange($scope.spanSelected, $scope.spanValueSelected, $scope.viewSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);


        };
        /* Called to update the url params based on the filter change and on initial page load
         * need to look into this*/
        $scope.updateURL = function (apply, changer) {

            $scope.spanValueList = $scope.spanValue[$scope.spanSelected];
            $scope.viewList = $scope.viewValue[$scope.spanSelected];

            /**  if ($scope.spanSelected == 'year') {
                $scope.year = $scope.spanValueSelected;
            } else if ($scope.spanSelected == 'week') {
                $scope.year = $scope.spanValueSelected.split['-'][2];
            } else if ($scope.spanSelected == 'quarter' || $scope.spanSelected == 'month') {
                $scope.year = '20' + $scope.spanValueSelected.split['-'][1];
            } **/

            if (changer == 'span') {
                $scope.projectSelected = 'all';
                $scope.resourceSelected = 'all';

                if ($scope.spanSelected == 'year') {
                    $scope.viewSelected = 'month';
                    $scope.spanValueSelected = $scope.currentFullYear.toString();
                } else if ($scope.spanSelected == 'quarter') {
                    $scope.spanValueSelected = $scope.currentYear + '-' + $scope.currentQuarter;
                    $scope.viewSelected = 'month';
                } else if ($scope.spanSelected == 'month') {
                    $scope.spanValueSelected = $scope.currentYear + '-' + $scope.currentMonth;
                    $scope.viewSelected = 'month';
                } else if ($scope.spanSelected == 'week') {
                    $scope.viewSelected = 'week';
                    $scope.spanValueSelected = getDateByWeek($scope.currentFullYear, $scope.currentWeek);
                } else if ($scope.spanSelected == 'day') {
                    $scope.spanValueSelected = 'day';
                    $scope.viewSelected = 'day';
                }

            }

            if (apply) {
                $scope.$apply(function () {
                    $log.info('UPDATE URL');
                    $log.info('$scope.spanSelected, $scope.spanValueSelected, $scope.viewSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected');
                    $log.info($scope.spanSelected, $scope.spanValueSelected, $scope.viewSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);
                    location_update();

                });
            } else {
                $log.info('UPDATE URL');
                $log.info('$scope.spanSelected, $scope.spanValueSelected, $scope.viewSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected');
                $log.info($scope.spanSelected, $scope.spanValueSelected, $scope.viewSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);
                location_update();

            }


        };

        /* location update utility*/
        var location_update = function () {

            $location.search('span', $scope.spanSelected);
            $location.search('span_value', $scope.spanValueSelected);
            $location.search('view_by', $scope.viewSelected);
            $location.search('cost_center', $scope.costCenterSelected);
            $location.search('project', $scope.projectSelected);
            $location.search('resource', $scope.resourceSelected);

            $log.info('$location.search');
            $log.info($location.search());


        };
        /* on location change call filter change with the updated params
         * */
        $scope.$on('$locationChangeSuccess', function (next, current) {
            $log.info('Location Change Called');
            var params = $location.search();
            if (params['span']) {
                $scope.spanSelected = params['span'];
                $scope.spanValueSelected = params['span_value'];
                $scope.viewSelected = params['view_by'];
                $scope.costCenterSelected = params['cost_center'];
                $scope.projectSelected = params['project'];
                $scope.resourceSelected = params['resource'];
                $scope.spanValueList = $scope.spanValue[$scope.spanSelected];
                $scope.viewList = $scope.viewValue[$scope.spanSelected];
            }

            $scope.filterChange($scope.spanSelected, $scope.spanValueSelected, $scope.viewSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);

        });

        /* API call function to get data
         * if resource is clicke do then display multichart else bar chart*/
        $scope.getData = function (spanSelected, spanValueSelected, viewSelected, costCenterSelected, projectSelected, resourceSelected) {
            $scope.fail = false;
            $('select').attr('disabled', true);

            $scope.totalCost = 0;
            $scope.costData = [];
            $scope.display_table = false;

            $('#d3-container').html('<div class="text-center panel-body">' + CU.Loading + '</div>');
            $('.nvtooltip').css('opacity', '0');
            UsageCost.getData(spanSelected, spanValueSelected, viewSelected, costCenterSelected, projectSelected, resourceSelected).then(function (value) {

                $('select').attr('disabled', false);

                /*if data is empty display message*/
                if (typeof(value.usage_data) != 'undefined' && value.usage_data.length > 0 && (value.usage ? value.usage.length > 0 : true)) {
                    $scope.display_table = true;

                    /* display the chart
                     * -- if resource is clicked then its day based*/
                    if (viewSelected == 'day') {
                        $log.info(' Day Selected do -- MULTI D3');
                        $scope.multid3(value.d3_json);
                        $scope.projectList = value.project_list;
                        $log.debug('PROJECT LIST --', $scope.projectList);
                        $scope.resourceList = value.resource_list;
                        $log.debug('Resource LIST --', $scope.resourceList);
                    }
                    else {
                        $log.info(' BAR CHART');
                        var data = value.usage_data;
                        $scope.projectList = [];
                        $scope.resourceList = [];
                        if ($scope.costCenterSelected != 'all') {

                            $scope.projectList = (value.project_list) ? value.project_list : [];
                            $log.debug('PROJECT LIST --', $scope.projectList);
                            $scope.resourceList = (value.resource_list) ? value.resource_list : [];
                            $log.debug('Resource LIST --', $scope.resourceList);
                        }
                        $scope.d3bar(value.usage_data);

                    }
                    $scope.costData = value.usage_data;

                    $.each(value.usage_data, function (k, v) {
                        $scope.totalCost += v.cost;
                    });

                    $scope.totalCost = parseFloat($scope.totalCost).toFixed(2);
                    $scope.fail = false;
                    $scope.monthName();

                } else {
                    $scope.fail = true;
                    $scope.loading = false;
                    $('#d3-container').html('');
                    $scope.class_name = 'blue';
                    $scope.message = $sce.trustAsHtml('No data available for the selected options.');
                }

            }, function (reason) {
                $('select').attr('disabled', false);
                var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
                $log.error('Reason for Failure ---', msg);
                $scope.fail = true;
                $scope.class_name = 'red';
                $('#d3-container').html('');
                $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);

            }, function (update) {
                $log.info('Update  ---', update);
            });

        };

        /* On year,month change
         * -- get the month,project and resource value
         * -- based on these make an api call to get  the data and display the chart*/

        $scope.filterChange = function (spanSelected, spanValueSelected, viewSelected, costCenterSelected, projectSelected, resourceSelected) {
            $log.info(' ++ FILTER CHANGE ++ ');
            $log.info(spanSelected, spanValueSelected, viewSelected, costCenterSelected, projectSelected, resourceSelected);

            $scope.getData(spanSelected, spanValueSelected, viewSelected, costCenterSelected, projectSelected, resourceSelected);

        };


        $scope.d3bar = function (data) {
            $('#d3-container').html('');
            var margin = {top: 20, right: 20, bottom: 30, left: 40}, width = 750 - margin.left - margin.right, height = 500 - margin.top - margin.bottom;

            var svg = d3.select("#d3-container").append("svg").attr('height', '600').style('height', '600px');

            var d3_data = [
                {
                    key: "Cumulative Return",
                    values: data
                }
            ];
            $log.debug('d3_data');
            $log.debug(d3_data);


            function Idlink(d) {
                if (d.toString().indexOf('ID') != -1 || d.toString().indexOf('hd') != -1) {
                    d3.selectAll(".nv-x .nv-axis .tick text").style('pointer-events', 'auto');
                    d3.selectAll(".nv-x .nv-axis .tick text").style('cursor', 'pointer');
                } else {
                    d3.selectAll(".nv-x .nv-axis .tick text").style('pointer-events', 'none');
                }
                return d;

            }

            nv.addGraph(function () {
                var chart = nv.models.discreteBarChart()
                    .x(function (d) {
                        return d.name
                    })
                    .y(function (d) {
                        return d.cost
                    })
                    .staggerLabels(true)
                    //.staggerLabels(historicalBarChart[0].values.length > 8)
                    .showValues(true)
                    .duration(250);


                chart.xAxis.tickFormat(function (d) {
                    return Idlink(d);
                });

                chart.rotateLabels(-45);
                chart.margin().bottom = 200;


                chart.yAxis.tickFormat(function (d) {
                    return d3.format("$,.2f")(d)
                });

                d3.select('#d3-container svg')
                    .datum(d3_data)
                    .call(chart);


                nv.utils.windowResize(chart.update);
                return chart;
            }, function () {
                d3.selectAll(".nv-bar").on('click',
                    function (e) {
                        /* make a call with this project id*/
                        var self = this;
                        var month_clicked = (($scope.spanSelected == 'year' || $scope.spanSelected == 'quarter') && $scope.viewSelected == 'month' );
                        var quarter_clicked = (($scope.spanSelected == 'year' || $scope.spanSelected == 'quarter') && $scope.viewSelected == 'quarter');
                        var week_clicked = (($scope.spanSelected == 'year' || $scope.spanSelected == 'month' || $scope.spanSelected == 'quarter') && $scope.viewSelected == 'week');
                        var project_clicked = ($scope.spanSelected == 'month' && $scope.projectSelected == 'all' && $scope.resourceSelected == 'all');
                        var resource_clicked = ($scope.spanSelected == 'month' && $scope.projectSelected != 'all' && $scope.resourceSelected == 'all');
                        /* month on the x-axis*/
                        if ($scope.costCenterSelected == 'all' && $scope.monthSelected != 'all') {
                            $scope.costCenterSelected = e.name;
                            $scope.projectSelected = 'all';
                            $scope.resourceSelected = 'all';
                            $log.debug('CENTER CLICKED');

                        } else if (quarter_clicked) {
                            $scope.spanSelected = 'quarter';
                            $scope.spanValueSelected = e.name;
                            $scope.viewSelected = 'month';
                            $log.debug('Quarter CLICKED');
                        } else if (month_clicked) {

                            $scope.spanSelected = 'month';
                            var year = e.name.split('-')[0];
                            var month = e.name.split('-')[1];
                            console.log(year);
                            console.log(month);

                            $.each($scope.months, function (k, value) {
                                if (month == value) {
                                    $scope.spanValueSelected = year + '-' + ( k + 1);
                                    return false;
                                }
                            });
                            $log.debug('MONTH CLICKED');
                        } else if (week_clicked) {
                            $scope.spanSelected = 'week';
                            $scope.spanValueSelected = e.name;
                            $log.debug('WEEK CLICKED');
                        } else if (project_clicked) {
                            $scope.projectSelected = e.name;
                            $log.debug('PROJECT CLICKED');
                        } else if (resource_clicked) {
                            $scope.resourceSelected = e.name;
                            $log.debug('RESOURCE CLICKED');
                        }

                        //$scope.getData($scope.yearSelected, $scope.monthSelected, $scope.projectSelected, $scope.resourceSelected);
                        $log.info($scope.spanSelected, $scope.spanValueSelected, $scope.viewSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);

                        $scope.updateURL(true);

                    });
                d3.selectAll(".nv-bar").style('cursor', 'pointer');
                /*
                 id links
                 */
                var project = false;
                d3.selectAll('.nv-x .nv-axis .tick text').on('click', function (e) {
                    var name, url, win;
                    if (e.indexOf('ID') != -1) {
                        name = e.split('-')[1];
                    } else {
                        name = e;
                    }
                    url = 'https://console.developers.google.com/project/' + name;
                    win = window.open(url, '_blank');
                    win.focus();
                }).on("mouseover", function () {
                    d3.select(this).style("fill", "blue");
                    d3.select(this).style("text-decoration", "underline");
                }).on("mouseout", function () {
                    d3.select(this).style("fill", "black");
                    d3.select(this).style("text-decoration", "none");
                });


            });

        };
        $scope.multid3 = function (data) {
            $('#d3-container').html('');
            var testdata = data.map(function (series) {
                series.values = series.values.map(function (d) {
                    var x = new Date(d[0]);
                    return {x: x.getTime(), y: d[1] }
                });
                return series;
            });
            var margin = {top: 20, right: 20, bottom: 30, left: 40}, width = 750 - margin.left - margin.right, height = 500 - margin.top - margin.bottom;

            var svg = d3.select("#d3-container").append("svg").attr('height', '600').style('height', '600px');
            var chart;
            nv.addGraph(function () {
                chart = nv.models.linePlusBarChart()
                    .margin({top: 50, right: 60, bottom: 30, left: 70})
                    .legendRightAxisHint(' [Using Right Axis]')
                    .color(d3.scale.category10().range())
                    .options({focusEnable: false});

                chart.xAxis
                    .tickFormat(function (d) {
                        return d3.time.format('%x')(new Date(d));
                    });
                chart.y1Axis.tickFormat(function (d) {
                    return d3.format("$,.2f")(d)
                });
                chart.y2Axis
                    .tickFormat(function (d) {

                        return $scope.format(d);
                    });


                chart.bars.forceY([0]).padData(false);

                /* chart.x2Axis.tickFormat(function (d) {
                 return d3.time.format('%x')(new Date(d))
                 }).showMaxMin(false);*/

                d3.select('#d3-container svg')
                    .datum(testdata)
                    .transition().duration(500).call(chart);

                nv.utils.windowResize(chart.update);

                return chart;
            });


        };
        $scope.format = function (d) {
            var isNeg = d < 0;
            if (d == 0) return '0';
            if (isNeg) {
                d = -d;
            }
            var k = 1000;
            var dm = 3;
            var sizes = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'];
            var i = Math.floor(Math.log(d) / Math.log(k));
            if (i < 0) {
                return d;
            }
            if (isNeg) {
                return -(d / Math.pow(k, i)).toPrecision(dm) + ' ' + sizes[i];
            } else {
                return (d / Math.pow(k, i)).toPrecision(dm) + ' ' + sizes[i];
            }
        };

        $scope.usage_display = function () {
            return ($scope.viewSelected == 'day');
        };


        $scope.monthName = function (month) {
            $.each($scope.months, function (k, value) {
                var name;
                if (month == (k + 1)) {
                    $scope.monthName = value;
                    return false;
                }
            });
        };

        /* utility to get the list of weeks for a given year*/
        var getWeeks = function (year, day) {
            var srt, i = 1, date;
            for (; i < 366 + 7; i++) {
                srt = new Date(year, 0, i - 6, 1);
                if (srt.getDay() == day && srt.getFullYear() <= year) {
                    date = (day == 0 ? $scope.months[srt.getMonth()] : styleDate(srt.getDate())) + '-' + (day == 0 ? styleDate(srt.getDate()) : $scope.months[srt.getMonth()]) + '-' + srt.getFullYear();
                    $scope.weekList[date] = date;
                }
            }
        };
        var styleDate = function (date) {
            return date > 9 ? date : '0' + date;
        };


        var getDateByWeek = function (year, week) {

            // Jan 1 of 'year'
            var d = new Date(year, 0, 1),
                offset = d.getTimezoneOffset();

            // ISO: week 1 is the one with the year's first Thursday
            // so nearest Thursday: current date + 4 - current day number
            // Sunday is converted from 0 to 7
            d.setDate(d.getDate() + 4 - (d.getDay() || 7));

            // 7 days * (week - overlapping first week)
            d.setTime(d.getTime() + 7 * 24 * 60 * 60 * 1000
                * (week + (year == d.getFullYear() ? -1 : 0 )));

            // daylight savings fix
            d.setTime(d.getTime()
                + (d.getTimezoneOffset() - offset) * 60 * 1000);

            // back to Monday (from Thursday)
            d.setDate(d.getDate() - 3);

            var date = d.toLocaleDateString("en-au", {year: "numeric", month: "short", day: "2-digit"}).replace(/\s/g, '-');

            return date;
        };

        /* init
         -- for setting all models
         -- get the data for current year and month -- yearChange*/
        $scope.init();
    }]);


Date.prototype.getWeek = function () {

    // Create a copy of this date object
    var target = new Date(this.valueOf());

    // ISO week date weeks start on monday, so correct the day number
    var dayNr = (this.getDay() + 6) % 7;

    // Set the target to the thursday of this week so the
    // target date is in the right year
    target.setDate(target.getDate() - dayNr + 3);

    // ISO 8601 states that week 1 is the week with january 4th in it
    var jan4 = new Date(target.getFullYear(), 0, 4);

    // Number of days between target date and january 4th
    var dayDiff = (target - jan4) / 86400000;

    if (new Date(target.getFullYear(), 0, 1).getDay() < 5) {
        // Calculate week number: Week 1 (january 4th) plus the
        // number of weeks between target date and january 4th
        return 1 + Math.ceil(dayDiff / 7);
    }
    else {  // jan 4th is on the next week (so next week is week 1)
        return Math.ceil(dayDiff / 7);
    }
};

