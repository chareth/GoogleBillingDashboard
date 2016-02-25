__author__ = "Ashwini Chandrasekar(@sriniash)"
__email__ = "ASHWINI_CHANDRASEKAR@homedepot.com"
__version__ = "1.0"
__doc__ = "Billing View API/HTML layer"

from flask import Blueprint, request
from flask.templating import render_template
from flask.wrappers import Response

import json
from apps.billing.billingData import get_project_list_data, get_center_list, \
    get_costs_per_center_year, \
    get_costs_per_project_year, get_costs_per_resource, get_costs_per_resource_per_project, \
    get_costs_per_resource_all_project_per_day, log, table_create, \
    get_project_by_id, update_project_data, \
    create_project_data, delete_project_by_id, \
    get_costs_year, get_costs_per_center_month, get_costs_per_cost_month, \
    get_costs_per_resource_month_center, get_costs_per_resource_per_project_per_day_month, get_costs_per_center_week, \
    get_costs_per_resource_week_center, get_costs_per_resource_per_project_per_day_week, \
    get_costs_per_resource_all_project_per_day_week, get_costs_per_center_year_quarter, \
    get_costs_per_resource_quarter_center, get_costs_per_resource_all_project_per_day_quarter, \
    get_costs_per_resource_per_project_per_day_quarter

from apps.config.apps_config import log
from apps.billing.dataProcessor import set_scheduler, run_scheduler, set_scheduler_initial

import datetime
import os


mod = Blueprint('billing', __name__, url_prefix='/billing')

set_scheduler_initial()

'''
    BILLING PAGE LANDING PAGE , COST CENTER PAGE AND API's
'''
# route handles for /admin and /admin/page
@mod.route('/')
def billing():
    url = 'billing/index.html'
    return render_template(url, title="Cloud Admin Tool")


# route handles for /admin and /admin/page
@mod.route('/cost_center/')
def cost_center_data():
    url = 'billing/cost_center_data.html'
    return render_template(url, title="Cloud Admin Tool")


# route handles for /admin and /admin/page
@mod.route('/projects')
def projects_cost_center():
    url = 'billing/projects.html'
    return render_template(url, title="Cloud Admin Tool")


# route handles for creating table for first time
@mod.route('/table')
def table():
    response = table_create()
    resp = Response(response=json.dumps(response),
                    status=200,
                    mimetype="application/json")

    return resp


# route handles for creating table for first time
@mod.route('/loadData', methods=['GET'])
def load_data():
    hour = request.args.get('hour', None)  # hour (0-23)
    min = request.args.get('min', None)  # minute (0-59)

    if hour is not None and min is not None:
        response = set_scheduler(hour, min)
        message = 'Job  is set  -- ' + str(response.get_jobs()) + ' to run everyday  at ' + hour + '.' + min
        os.environ['SCHEDULER_HOUR'] = hour
        os.environ['SCHEDULER_MIN'] = min
    else:
        response = run_scheduler()
        message = 'Job  is set to run now ' + str(datetime.datetime.now()) + ' and next run is at ' + \
                  str(os.environ.get('SCHEDULER_HOUR')) + '.' + str(os.environ.get('SCHEDULER_MIN'))

    resp = Response(response=json.dumps(message),
                    status=200,
                    mimetype="application/json")

    return resp


'''

    API to get the list of distinct projects

'''


@mod.route('/usage/projects', methods=['GET'])
def get_project_list():
    data = get_project_list_data()

    resp = Response(response=json.dumps(data['data']),
                    status=data['status'],
                    mimetype="application/json")
    return resp


'''
    API that acts as a router to all the other calls based on the filter values year, month, project and resource
    Main entry point
    inputs : Year in the url
    params: month,cost_center,project,resource
    output : JSON with usage_data for all calls, project_list and resource_list in calls that need them

    /billing/usage/2015
        --> get_costs_per_month(year)

'''


@mod.route('/usage/<int:year>', methods=['GET'])
def get_costs(year):
    log.info('-----------In get_costs-----------------------')
    log.info(year)
    project_list_local = dict()
    data = dict(usage_data=[], status=200)

    span = request.args.get('span')
    span_value = request.args.get('span_value')
    view_by = request.args.get('view_by')
    cost_center = request.args.get('cost_center')
    project = request.args.get('project')
    resource = request.args.get('resource')

    log.info('year,span,span_value,view_by,cost_center,project,resource')
    log.info('{0} -{1} -{2} -{3} -{4}-{5}-{6}'.format(year, span, span_value, view_by, cost_center, project, resource))

    '''
        get the project id from the center list that has the name if name was passed in as db needs id
    '''
    cost_center_list = get_center_list(False)
    for project_info in cost_center_list:
        project_list_local[project_info['project_id']] = project_info['project_name']

    for project_id in project_list_local:
        if project_list_local[project_id] == project:
            project = project_id

    if span == 'month' or span == 'quarter':
        span_value = span_value.split('-')[1]
    elif span == 'week':
        month = month_converter(span_value.split('-')[1])
        date = span_value.split('-')[0]
        '''
           sql starts with 0-52
           python/js -- 1-53
        '''
        span_value = datetime.date(int(year), int(month), int(date)).isocalendar()[1] - 1

    try:

        if span == 'year':
            if cost_center == 'all' and project == 'all' and resource == 'all':
                log.info('cost_center == all and project == all and resource == all')
                data = get_costs_per_cost_month(year, span_value, view_by)

            elif cost_center != 'all' and project == 'all' and resource == 'all':
                log.info('cost_center != all and project == all and resource == all')
                data = get_costs_per_center_year(year, cost_center, view_by)

            elif cost_center != 'all' and project != 'all' and resource == 'all':
                log.info('cost_center != all and project != all and resource == all')
                data = get_costs_per_project_year(year, cost_center, project, view_by)

            elif cost_center != 'all' and project != 'all' and resource != 'all':
                log.info('cost_center != all and project != all and resource != all')
                data = get_costs_per_resource_per_project(year, cost_center, project,
                                                          resource, view_by)
            elif cost_center != 'all' and project == 'all' and resource != 'all':
                log.info('cost_center != all and project == all and resource != all')
                data = get_costs_per_resource(year, cost_center, resource, view_by)

        elif span == 'month':
            if cost_center == 'all' and project == 'all' and resource == 'all':
                log.info('cost_center == all and project == all and resource == all')
                data = get_costs_per_cost_month(year, span_value, view_by)

            elif cost_center != 'all' and project == 'all' and resource == 'all':
                log.info('cost_center != all and project == all and resource == all')
                data = get_costs_per_center_month(year, span_value, cost_center, view_by)

            elif cost_center != 'all' and project != 'all' and resource == 'all':
                log.info('cost_center != all and project != all and resource == all')
                data = get_costs_per_resource_month_center(year, span_value, cost_center, project, view_by)

            elif cost_center != 'all' and project != 'all' and resource != 'all':
                log.info('cost_center != all and project != all and resource != all')
                data = get_costs_per_resource_per_project_per_day_month(year, span_value, cost_center, project,
                                                                        resource, view_by)

            elif cost_center != 'all' and project == 'all' and resource != 'all':
                log.info('cost_center != all and project == all and resource != all')
                data = get_costs_per_resource_all_project_per_day(year, span_value, cost_center, resource, view_by)

        elif span == 'week':
            if cost_center == 'all' and project == 'all' and resource == 'all':
                log.info('cost_center == all and project == all and resource == all')
                data = get_costs_per_cost_month(year, span_value, view_by)

            elif cost_center != 'all' and project == 'all' and resource == 'all':
                log.info('cost_center != all and project == all and resource == all')
                data = get_costs_per_center_week(year, span_value, cost_center, view_by)

            elif cost_center != 'all' and project != 'all' and resource == 'all':
                log.info('cost_center != all and project != all and resource == all')
                data = get_costs_per_resource_week_center(year, span_value, cost_center, project, view_by)

            elif cost_center != 'all' and project != 'all' and resource != 'all':
                log.info('cost_center != all and project != all and resource != all')
                data = get_costs_per_resource_per_project_per_day_week(year, span_value, cost_center, project,
                                                                       resource, view_by)

            elif cost_center != 'all' and project == 'all' and resource != 'all':
                log.info('cost_center != all and project == all and resource != all')
                data = get_costs_per_resource_all_project_per_day_week(year, span_value, cost_center, resource, view_by)

        elif span == 'quarter':
            if cost_center == 'all' and project == 'all' and resource == 'all':
                log.info('cost_center == all and project == all and resource == all')
                data = get_costs_per_cost_month(year, span_value, view_by)

            elif cost_center != 'all' and project == 'all' and resource == 'all':
                log.info('cost_center != all and project == all and resource == all')
                data = get_costs_per_center_year_quarter(year, span_value, cost_center, view_by)

            elif cost_center != 'all' and project != 'all' and resource == 'all':
                log.info('cost_center != all and project != all and resource == all')
                data = get_costs_per_resource_quarter_center(year, span_value, cost_center, project, view_by)

            elif cost_center != 'all' and project != 'all' and resource != 'all':
                log.info('cost_center != all and project != all and resource != all')
                data = get_costs_per_resource_per_project_per_day_quarter(year, span_value, cost_center, project,
                                                                          resource, view_by)

            elif cost_center != 'all' and project == 'all' and resource != 'all':
                log.info('cost_center != all and project == all and resource != all')
                data = get_costs_per_resource_all_project_per_day_quarter(year, span_value, cost_center, resource,
                                                                          view_by)

        else:
            log.info('Outside all conditions')

        resp = Response(response=json.dumps(data['data']),
                        status=data['status'],
                        mimetype="application/json")

    except Exception as e:
        log.error('Error in get_costs() -- {0}'.format(e[0]))
        data['message'] = e[0]
        resp = Response(response=json.dumps(data),
                        status=500,
                        mimetype="application/json")

    return resp


def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1


'''
            PROJECT INFO CREATION PAGE AND API's
'''

'''
    API for the adding project into cost_center or getting Cost Center Data

    GET -- /usage/cost_center?unique=true --> for array of unique cost_center names
    GET -- /usage/cost_center--> list of dict of projects details

    POST -- /usage/cost_center-->
           I/P:
                json:
                {
                    "projects" :[
                    {"project_id":"ID-12345","project_name":"lab","cost_center":"Aurora","director":""},
                    {"project_id":"ID-123456","project_name":"demo","cost_center":"Aurora","director":""},
                    {"project_id":"ID-1234567","project_name":"dev","cost_center":"Aurora","director":""},
                    {"project_id":"ID-12345678","project_name":"prod","cost_center":"Aurora","director":""}
                    ]

                }
            O/P:
                 {
                    'message': ' cost_center_list Created/Updated'
                 }



'''


@mod.route('/usage/cost_center', methods=['POST', 'GET'])
def get_cost_center_list():
    cost_center_list = []

    if request.method == 'GET':
        unique = request.args.get('unique', False)

        try:
            if unique:
                cost_center_list = get_center_list(unique)
            else:
                cost_center_list = get_center_list(False)

            status = 200
            response = {
                'cost_center_list': cost_center_list
            }

        except Exception as e:
            log.error('Error in getting  group List -- {0}'.format(e))
            status = 500
            response = {
                'message': str(e)
            }

    else:
        try:
            projects = request.json['projects']

            for project in projects:
                project_id = project['project_id']
                project_name = project['project_name'].lower()
                cost_center = project['cost_center'].lower()
                director = project['director'].lower()
                director_email = project['director_email'].lower()
                contact_name = project['contact_name'].lower()
                contact_email = project['contact_email'].lower()
                alert_amount = 0  # project['alert_amount'].lower()

                if not director.strip():
                    director = None
                if not contact_name.strip():
                    contact_name = None
                if not contact_email.strip():
                    contact_email = None
                if not director_email.strip():
                    director_email = None
                '''
                    if not alert_amount.strip():
                       alert_amount = 'None'
                '''

                '''
                    Check if project already in the table
                '''
                query_data = get_project_by_id(project_id)

                if len(query_data) > 0:
                    log.info('DATA IN TABLE - SO UPDATE')
                    query_data = update_project_data(cost_center, project_id, project_name, director, director_email,
                                                     contact_name, contact_email, alert_amount)

                else:
                    log.info('DATA NOT IN TABLE - SO INSERT')
                    query_data = create_project_data(cost_center, project_id, project_name, director, director_email,
                                                     contact_name, contact_email, alert_amount)

            status = 200
            response = {
                'message': ' cost_center_list Created/Updated'
            }
        except Exception as e:
            log.error('Error in creating  group List -- {0}'.format(e))
            status = 500
            response = {
                'message': str(e[0]),
                'cost_center_list': cost_center_list
            }

    resp = Response(response=json.dumps(response),
                    status=status,
                    mimetype="application/json")

    return resp


'''
    API for the deleting project into cost_center
    POST -- /usage/cost_center/delete -->
           I/P:
                json:
              {
                "projects" :["ID-12345","ID-123456","ID-1234567"]

                }
            O/P:
                 {
                    'message': ' Projects Deleted'
                 }



'''


@mod.route('/usage/cost_center/delete', methods=['POST'])
def delete_cost_center_project():
    cost_center_list = []
    try:
        projects = request.json['projects']

        for project_id in projects:
            query = delete_project_by_id(project_id)

        status = 200
        response = {
            'message': ' cost_center_list Deleted'
        }
    except Exception as e:
        log.error('Error in creating  group List -- {0}'.format(e))
        status = 500
        response = {
            'message': str(e),
            'cost_center_list': cost_center_list
        }

    resp = Response(response=json.dumps(response),
                    status=status,
                    mimetype="application/json")

    return resp
