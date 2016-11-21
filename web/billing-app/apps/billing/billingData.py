__author__ = "Ashwini Chandrasekar(@sriniash)"
__email__ = "ASHWINI_CHANDRASEKAR@homedepot.com"
__version__ = "1.0"
__doc__ = "Data Layer that is used by view and this makes call to the billingDBQuery"

import time, json
from decimal import Decimal
from datetime import date, timedelta
import traceback
from apps.config.apps_config import log_error, log_output, log
from apps.billing.billingDBQuery import get_distinct_projects, get_resource_list_per_project, get_billing_data_per_year, \
    get_billing_data_per_year_per_center, get_billing_data_per_project_year, get_billing_data_per_resource, \
    get_billing_data_per_resource_per_project, \
    get_cost_centers, create_table, get_project, update_project, create_project, delete_project, AlchemyEncoder, \
    set_global_cost_center_list, \
    get_billing_data_per_year_per_center_days, get_billing_data_per_year_per_center_quarter, \
    get_billing_data_per_year_month, get_billing_data_per_year_month_week_day, \
    get_billing_data_per_resource_month_center, \
    get_billing_data_per_resource_month_week_day_center, get_billing_data_per_resource_all_project_per_day_month, \
    get_billing_data_per_resource_per_project_per_month, get_billing_data_per_year_week_day, \
    get_billing_data_per_resource_week_day_center, get_billing_data_per_resource_per_project_per_week, \
    get_billing_data_per_resource_all_project_per_day_week, get_billing_data_per_year_quarter_week_day, \
    get_billing_data_per_resource_all_project_per_day_quarter, get_billing_data_per_resource_per_project_per_quarter


'''
    Global values center
'''

'''
    get the list of projects
'''


def get_project_list_data():
    project_list = dict()
    status = 200
    project_names = []

    try:
        log.info('In Project List Data ----')

        projects = get_distinct_projects()
        cost_center_projects = set_global_cost_center_list()

        for (project) in projects:
            for center in cost_center_projects:
                center_data = json.loads(json.dumps(center, cls=AlchemyEncoder))
                if project[0] == center_data['project_id']:
                    project_list[project[0]] = center_data['project_name']
                elif project[0] not in project_list:
                    project_list[project[0]] = project[0]

        for (id, names) in project_list.iteritems():
            project_names.append(names)
    except Exception as e:
        log_error(e[0])
        status = 500
        project_list['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=project_names, status=status)

    return response


'''
 Get project list based on the center
 input -- center
 output --> dict with lists array and id string

'''


def project_list_per_center(center):
    log.info(' IN PROJECT LIST PER CENTER __ {0}'.format(center))
    project_list_center = ''
    project_list_center_arr = []
    project_list_center_arr_id = []
    project_center_all_list = []
    project_list_local = []
    status = 200

    try:
        cost_center_list = set_global_cost_center_list()

        for project in cost_center_list:
            project_center_all_list.append(project['project_id'])
            if project['cost_center'] == center:
                project_list_center += ",'" + project['project_id'] + "'"
                if center.lower() == 'other' and project['project_name'] == project['project_id']:
                    project_list_center_arr.append(project['project_id'])
                else:
                    project_list_center_arr.append(project['project_name'])

                project_list_center_arr_id.append(project['project_id'])

        project_list_local = project_list_center_arr
    except Exception as e:
        status = 500
        traceback.print_exc()

    return {'list': project_list_local, 'ids': project_list_center_arr_id, 'data': project_list_center_arr,
            'status': status}


'''
  get resource list based on project id

  if project_name is used the n get the id from the cost center else id will be sent
'''


def resource_list_per_project(center, project):
    resource_list = []
    project_list_local = {}

    log.info('IN RESOURCE_LIST_PER_PROJECT -- {0} -- {1}'.format(center, project))

    cost_center_list = set_global_cost_center_list()

    for project_info in cost_center_list:
        project_list_local[project_info['project_id']] = project_info['project_name']

    if project is not None:
        for project_id in project_list_local:
            if project_list_local[project_id] == project:
                project = str(project_id)

        query_data = get_resource_list_per_project([project])

    else:
        project_ids = project_list_per_center(center)['ids']
        query_data = get_resource_list_per_project(project_ids)

    log_output('In resource List')
    log_output(query_data)

    for (resource) in query_data:
        resource_list.append(resource[0])

    return resource_list


'''
  utility to get month/quarter based data
'''


def get_per_month_cost(query_data, quarter, year):
    log.info('get_per_month_cost == {0}'.format(query_data))

    year = str(year)

    per_month_data = [{'cost': float(0), 'name': year[-2:] + '-Jan', 'month': '1'},
                      {'cost': float(0), 'name': year[-2:] + '-Feb', 'month': '2'},
                      {'cost': float(0), 'name': year[-2:] + '-Mar', 'month': '3'},
                      {'cost': float(0), 'name': year[-2:] + '-Apr', 'month': '4'},
                      {'cost': float(0), 'name': year[-2:] + '-May', 'month': '5'},
                      {'cost': float(0), 'name': year[-2:] + '-Jun', 'month': '6'},
                      {'cost': float(0), 'name': year[-2:] + '-Jul', 'month': '7'},
                      {'cost': float(0), 'name': year[-2:] + '-Aug', 'month': '8'},
                      {'cost': float(0), 'name': year[-2:] + '-Sep', 'month': '9'},
                      {'cost': float(0), 'name': year[-2:] + '-Oct', 'month': '10'},
                      {'cost': float(0), 'name': year[-2:] + '-Nov', 'month': '11'},
                      {'cost': float(0), 'name': year[-2:] + '-Dec', 'month': '12'}]

    per_quarter_data = dict()

    per_quarter_data['1'] = [{'cost': float(0), 'name': year[-2:] + '-Jan', 'month': '1'},
                             {'cost': float(0), 'name': year[-2:] + '-Feb', 'month': '2'},
                             {'cost': float(0), 'name': year[-2:] + '-Mar', 'month': '3'}]
    per_quarter_data['2'] = [{'cost': float(0), 'name': year[-2:] + '-Apr', 'month': '4'},
                             {'cost': float(0), 'name': year[-2:] + '-May', 'month': '5'},
                             {'cost': float(0), 'name': year[-2:] + '-Jun', 'month': '6'}]
    per_quarter_data['3'] = [{'cost': float(0), 'name': year[-2:] + '-Jul', 'month': '7'},
                             {'cost': float(0), 'name': year[-2:] + '-Aug', 'month': '8'},
                             {'cost': float(0), 'name': year[-2:] + '-Sep', 'month': '9'}]
    per_quarter_data['4'] = [{'cost': float(0), 'name': year[-2:] + '-Oct', 'month': '10'},
                             {'cost': float(0), 'name': year[-2:] + '-Nov', 'month': '11'},
                             {'cost': float(0), 'name': year[-2:] + '-Dec', 'month': '12'}]

    if quarter is not None:
        for (month, cost) in query_data:
            for val in per_quarter_data[str(quarter)]:
                if val['month'] == str(month):
                    val['cost'] = float(cost)
        return per_quarter_data[str(quarter)]
    else:
        for (month, cost) in query_data:
            for val in per_month_data:
                if val['month'] == str(month):
                    val['cost'] = float(cost)
        return per_month_data


'''
    utility to create usage data
'''


def get_usage_data(query_data):
    usage_data = []
    for (week, cost) in query_data:
        data = dict(name=week, cost=cost)
        usage_data.append(data)
    return usage_data


'''
    utility to create quarter data
'''


def get_quarter_data(year, query_data):
    usage_data = []
    year = str(year)
    for (quarter, cost) in query_data:
        val = year[-2:] + '-' + str(quarter)
        data = dict(name=val, cost=cost)
        usage_data.append(data)
    return usage_data


'''
    utility to get data per day
'''


def get_per_day_data(query_data):
    usage_data = []
    d3_json = [{'key': 'Cost', 'values': [], 'bar': True}, {'key': 'Usage', 'values': []}]
    for (timestamp, cost, use, unit) in query_data:
        value = []
        date = time.strftime("%x", time.localtime(int(timestamp)))
        value.append(date)
        value.append(float(cost))
        value.append('$')
        d3_json[0]['values'].append(value)
        value = []
        value.append(date)
        value.append(float(use))
        value.append(str(unit))
        d3_json[1]['values'].append(value)

        day_data = dict(name=date, cost=float(cost), usage=float(use), unit=str(unit))
        usage_data.append(day_data)

    return {'usage_data': usage_data, 'd3_json': d3_json}


def get_week_days(year, week):
    d = date(year, 1, 1)
    if d.weekday() > 3:
        d = d + timedelta(7 - d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt, d + dlt + timedelta(days=6)


'''
  Utility to get week date
'''


def get_week_data(query_data, year, cost_center_projects_id):
    week_output = []
    week_data = []
    for week in range(0, 53):
        week_data.append(dict(name=week, cost=float(0)))
    if cost_center_projects_id is not None:
        for (project, week_no, cost) in query_data:
            if project in cost_center_projects_id:
                for week in week_data:
                    if week['name'] == week_no:
                        real_week = week_no + 1
                        week['date'] = get_week_days(year, real_week)[0].strftime("%d-%b-%Y")
                        week['cost'] += cost
    else:
        for (project, week_no, cost) in query_data:
            for week in week_data:
                if week['name'] == week_no:
                    real_week = week_no + 1
                    week['date'] = get_week_days(year, real_week)[0].strftime("%d-%b-%Y")
                    week['cost'] += cost

    for week in week_data:
        if week['cost'] != 0.0:
            week_output.append(week)
            week['name'] = week['date']

    return week_output


'''
  For getting costs of projects  for a year
  output_type : 'month' or 'week' or 'quarter'


'''


def get_costs_year(year, output_type):
    data = dict()
    usage_data = []
    status = 200

    log.info(' In get_costs_year == {0} -- {1}'.format(year, output_type))
    try:
        query_data = get_billing_data_per_year(str(year), output_type)
        log_output(query_data)
        data = {
            'usage_data': usage_data
        }

        if output_type == 'month':
            usage_data = get_per_month_cost(query_data, None, year)
            data['usage_data'] = usage_data
        elif output_type == 'week' or output_type == 'quarter':
            usage_data = get_usage_data(query_data)
            data['usage_data'] = usage_data
        elif output_type == 'day':
            day_data = get_per_day_data(query_data)
            data['usage_data'] = day_data['usage_data']
            data['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        data['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=data, status=status)

    return response


'''
     for getting aggregated cost of each cost center  for that year
     output_type ='month' or 'week' or 'day' or 'quarter'
'''


def get_costs_per_center_year(year, center, output_type):
    log.info('get_costs_per_center_year == {0}--{1} --{2}'.format(year, center, output_type))
    data = dict()
    usage_data = []
    status = 200

    try:

        project_list_local = project_list_per_center(center)['list']
        project_ids = project_list_per_center(center)['ids']
        resource_list_local = resource_list_per_project(center, None)

        data = {
            'usage_data': usage_data,
            'project_list': project_list_local,
            'resource_list': resource_list_local

        }
        if output_type == 'month':
            query_data = get_billing_data_per_year_per_center(str(year), project_ids, output_type)
            log_output(query_data)
            usage_data = get_per_month_cost(query_data, None, year)
            data['usage_data'] = usage_data

        elif output_type == 'week':
            query_data = get_billing_data_per_year_per_center(str(year), project_ids, output_type)
            log_output(query_data)
            usage_data = get_week_data(query_data, year, None)
            data['usage_data'] = usage_data

        elif output_type == 'quarter':
            query_data = get_billing_data_per_year_per_center(str(year), project_ids, output_type)
            log_output(query_data)
            usage_data = get_quarter_data(year, query_data)
            data['usage_data'] = usage_data

        elif output_type == 'day':
            query_data = get_billing_data_per_year_per_center_days(str(year), project_ids)
            log_output(query_data)
            day_data = get_per_day_data(query_data)
            data['usage_data'] = day_data['usage_data']
            data['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        data['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=data, status=status)

    return response


'''
    for getting aggregated cost of each project for each month
'''


def get_costs_per_project_year(year, center, project, output_type):
    log.info('get_costs_per_project_year == {0}--{1} --{2} --{3}'.format(year, center, project, output_type))

    data_json = dict()
    usage_data = []
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        resource_list_local = resource_list_per_project(center, None)

        query_data = get_billing_data_per_project_year(str(year), str(project), output_type)
        log_output(query_data)

        data_json = {
            'usage_data': usage_data,
            'project_list': project_list_local,
            'resource_list': resource_list_local
        }
        if output_type == 'month':
            usage_data = get_per_month_cost(query_data, None, year)
            data_json['usage_data'] = usage_data
        elif output_type == 'week':
            usage_data = get_week_data(query_data, year, None)
            data_json['usage_data'] = usage_data
        elif output_type == 'quarter':
            usage_data = get_quarter_data(year, query_data)
            data_json['usage_data'] = usage_data

        elif output_type == 'day':
            day_data = get_per_day_data(query_data)
            data_json['usage_data'] = day_data['usage_data']
            data_json['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        data_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=data_json, status=status)

    return response


'''
    API for getting  cost of a resource for a project for all months
'''


def get_costs_per_resource_per_project(year, center, project, resource, output_type):
    log.info('get_costs_per_resource_per_project == {0}--{1} --{2} --{3}--{4} '.format(year, center, project, resource,
                                                                                       output_type))

    resource_json = dict()
    usage_data = []
    status = 200

    project_list_local = project_list_per_center(center)['list']
    resource_list_local = resource_list_per_project(center, project)

    try:
        query_data = get_billing_data_per_resource_per_project(str(year), str(project), str(resource), output_type)
        log_output(query_data)
        resource_json = {
            'usage_data': usage_data,
            'project_list': project_list_local,
            'resource_list': resource_list_local

        }

        if output_type == 'month':
            usage_data = get_per_month_cost(query_data, None, year)
            resource_json['usage_data'] = usage_data

        elif output_type == 'week':
            usage_data = get_week_data(query_data, year, None)
            resource_json['usage_data'] = usage_data
        elif output_type == 'quarter':
            usage_data = get_quarter_data(year, query_data)
            resource_json['usage_data'] = usage_data
        elif output_type == 'day':
            day_data = get_per_day_data(query_data)
            resource_json['usage_data'] = day_data['usage_data']
            resource_json['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        resource_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=resource_json, status=status)

    return response


'''
    API for getting  cost of a resource all months

'''


def get_costs_per_resource(year, center, resource, output_type):
    log.info('get_costs_per_resource == {0}--{1} --{2} --{3} '.format(year, center, resource, output_type))

    resource_json = dict()
    usage_data = []
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        project_ids = project_list_per_center(center)['ids']
        resource_list_local = resource_list_per_project(center, None)

        query_data = get_billing_data_per_resource(str(year), project_ids, str(resource), output_type)
        log_output(query_data)

        resource_json = {
            'usage_data': usage_data,
            'project_list': project_list_local,
            'resource_list': resource_list_local
        }

        if output_type == 'month':
            usage_data = get_per_month_cost(query_data, None, year)
            resource_json['usage_data'] = usage_data
        elif output_type == 'week':
            usage_data = get_week_data(query_data, year, None)
            resource_json['usage_data'] = usage_data
        elif output_type == 'quarter':
            usage_data = get_quarter_data(year, query_data)
            resource_json['usage_data'] = usage_data
        elif output_type == 'day':
            day_data = get_per_day_data(query_data)
            resource_json['usage_data'] = day_data['usage_data']
            resource_json['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        resource_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=resource_json, status=status)

    return response


'''
     for getting aggregated cost of each project for that month/week/quarter send based on cost center
     output_type : 'month' or 'week' or 'day'

     fix for week and day values for all centers

'''


def get_costs_per_cost_month(year, value_to_match, output_type):
    log.info('get_costs_per_cost_month == {0}--{1} --{2}'.format(year, value_to_match, output_type))
    month_json = dict()
    month_data = []
    status = 200
    try:
        cost_center_list = set_global_cost_center_list()
        new_dict = dict()
        projects_list = []
        month_json = {
            'usage_data': month_data
        }

        for project_info in cost_center_list:
            projects_list.append(str(project_info['project_id']))

        query_data = get_billing_data_per_year_month(str(year), str(value_to_match), str(output_type))
        log_output(query_data)

        if query_data is not None:

            for (project, cost) in query_data:
                for project_info in cost_center_list:
                    cost_center = str(project_info['cost_center'])
                    project_id = str(project_info['project_id'])
                    owner = str(project_info['owner'])

                    if project == project_id:
                        new_dict[cost_center] = new_dict.get(cost_center, {})
                        new_dict[cost_center]['owner'] = owner
                        new_dict[cost_center]['cost'] = new_dict[cost_center].get('cost', 0.0)
                        new_dict[cost_center]['project'] = new_dict[cost_center].get('project', [])
                        new_dict[cost_center]['project'].append(str(project))
                        new_dict[cost_center]['cost'] += cost

            get_total_budgets(new_dict, cost_center_list)

            for key, value in new_dict.items():
                each_month = dict(name=value['owner'], cost=value['cost'], id=key, \
                    total_budget=value['total_budget'], percentage=value['percentage'])
                month_data.append(each_month)

        month_json['usage_data'] = month_data

        month_json = {
            'usage_data': month_data
        }

    except Exception as e:

        log_error(e[0])
        status = 500
        month_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=month_json, status=status)

    return response


'''
    for summing the toal budget for each cost center and
    calculating percentage of budget used
    only give total if every project has a budget
'''

def get_total_budgets(data, projectsTable):
    for cost_center in data:
        filtered_projects = filter(lambda x: x['project_id'] in data[cost_center]['project'], projectsTable)
        alert_amounts = [Decimal(x['alert_amount']) for x in filtered_projects]

        # if all projects have an alert_amount then sum them up
        if all(map(lambda x: not(x['alert_amount'] == 0 or x['alert_amount'] == '' or x['alert_amount'] == None), filtered_projects)):
            data[cost_center]['total_budget'] = str(reduce(lambda x, y: x + y, alert_amounts))
            data[cost_center]['percentage'] = data[cost_center]['cost'] / float(data[cost_center]['total_budget']) * 100
        else :
            data[cost_center]['total_budget'] = ""
            data[cost_center]['percentage'] = ""




'''
     for getting aggregated cost of each cost center
     output_type : 'month' or 'week' or'day'
     month value is sent to match
'''


def get_costs_per_center_month(year, month, center, output_type):
    log.info(
        'get_costs_per_center_month == {0}--{1} --{2} --{3}'.format(year, month, center, output_type))
    center_json = dict()
    status = 200

    try:


        cost_center_list = set_global_cost_center_list()
        project_list_local = project_list_per_center(center)['list']
        project_id_local = project_list_per_center(center)['ids']
        resource_list_local = resource_list_per_project(center, None)
        cost_center_projects_id = []
        cost_center_projects_name = []

        for project_info in cost_center_list:
            if project_info['cost_center'] == center:
                cost_center_projects_id.append(project_info['project_id'])
                cost_center_projects_name.append(project_info['project_name'])

        month_data = []
        center_json = {
            'usage_data': month_data,
            'project_list': project_list_local,
            'resource_list': resource_list_local

        }
        if output_type == 'month':


            query_data = get_billing_data_per_year_month(str(year), str(month), str(output_type))
            log_output(query_data)

            for (project, cost) in query_data:
                if project in cost_center_projects_id:
                    if cost_center_projects_name[cost_center_projects_id.index(project)].lower() == 'none':
                        name = project
                    else:
                        name = cost_center_projects_name[cost_center_projects_id.index(project)]
                    each_month = {'name': name,
                                  'cost': float(cost)}
                    month_data.append(each_month)
            center_json['usage_data'] = month_data

        elif output_type == 'week':
            query_data = get_billing_data_per_year_month_week_day(str(year), str(month), str(output_type),
                                                                  project_id_local)
            log_output(query_data)

            center_json['usage_data'] = get_week_data(query_data, year, cost_center_projects_id)

        elif output_type == 'day':
            query_data = get_billing_data_per_year_month_week_day(str(year), str(month), str(output_type),
                                                                  project_id_local)
            log_output(query_data)
            day_data = get_per_day_data(query_data)
            center_json['usage_data'] = day_data['usage_data']
            center_json['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        center_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=center_json, status=status)

    return response


'''
     for getting aggregated cost of each cost center
     output_type : 'month' or 'week' or'day'
     month value is sent to match
'''


def get_costs_per_center_week(year, week, center, output_type):
    log.info(
        'get_costs_per_center_week == {0}--{1} --{2} --{3}'.format(year, week, center, output_type))
    center_json = dict()
    status = 200
    try:


        cost_center_list = set_global_cost_center_list()
        project_list_local = project_list_per_center(center)['list']
        project_id_local = project_list_per_center(center)['ids']
        resource_list_local = resource_list_per_project(center, None)
        cost_center_projects_id = []
        cost_center_projects_name = []

        for project_info in cost_center_list:
            if project_info['cost_center'] == center:
                cost_center_projects_id.append(project_info['project_id'])
                cost_center_projects_name.append(project_info['project_name'])

        week_output = []
        center_json = {
            'usage_data': week_output,
            'project_list': project_list_local,
            'resource_list': resource_list_local

        }
        if output_type == 'week':
            query_data = get_billing_data_per_year_week_day(str(year), str(week), str(output_type), project_id_local)
            log_output(query_data)

            center_json['usage_data'] = get_week_data(query_data, year, cost_center_projects_id)

        elif output_type == 'day':
            query_data = get_billing_data_per_year_week_day(str(year), str(week), str(output_type), project_id_local)
            log_output(query_data)

            day_data = get_per_day_data(query_data)
            center_json['usage_data'] = day_data['usage_data']
            center_json['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        center_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=center_json, status=status)

    return response


'''
    API for getting aggregated cost of each resource for a project for that month
'''


def get_costs_per_resource_month_center(year, value_to_match, center, project, output_type):
    log.info(
        'get_costs_per_resource_month_center == {0}--{1} --{2} --{3} -- {4}'.format(year, value_to_match, center,
                                                                                    project, output_type))

    project_json = dict()
    usage_data = []
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        resource_list_local = resource_list_per_project(center, project)

        project_json = {
            'usage_data': usage_data,
            'resource_list': resource_list_local,
            'project_list': project_list_local
        }

        if output_type == 'month':
            query_data = get_billing_data_per_resource_month_center(str(year), str(value_to_match), str(project),
                                                                    output_type)
            log_output(query_data)
            usage_data = get_usage_data(query_data)
            project_json['usage_data'] = usage_data
        elif output_type == 'week':
            query_data = get_billing_data_per_resource_month_week_day_center(str(year), str(value_to_match),
                                                                             str(project),
                                                                             output_type)
            log_output(query_data)

            project_json['usage_data'] = get_week_data(query_data, year, None)

        elif output_type == 'day':
            query_data = get_billing_data_per_resource_month_week_day_center(str(year), str(value_to_match),
                                                                             str(project),
                                                                             output_type)
            log_output(query_data)

            day_data = get_per_day_data(query_data)
            project_json['usage_data'] = day_data['usage_data']
            project_json['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        project_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=project_json, status=status)

    return response


'''
    API for getting aggregated cost of each resource for a project for that month
'''


def get_costs_per_resource_quarter_center(year, quarter, center, project, output_type):
    log.info(
        'get_costs_per_resource_month_center == {0}--{1} --{2} --{3} -- {4}'.format(year, quarter, center,
                                                                                    project, output_type))

    project_json = dict()
    usage_data = []
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        resource_list_local = resource_list_per_project(center, project)

        project_json = {
            'usage_data': usage_data,
            'resource_list': resource_list_local,
            'project_list': project_list_local
        }

        if output_type == 'month':
            query_data = get_billing_data_per_year_quarter_week_day(str(year), str(quarter), str(project),
                                                                    output_type)
            log_output(query_data)

            usage_data = get_per_month_cost(query_data, quarter, year)
            project_json['usage_data'] = usage_data

        elif output_type == 'week':
            query_data = get_billing_data_per_year_quarter_week_day(str(year), str(quarter),
                                                                    str(project),
                                                                    output_type)
            log_output(query_data)

            usage_data = get_week_data(query_data, year, None)

            project_json['usage_data'] = usage_data

        elif output_type == 'day':
            query_data = get_billing_data_per_year_quarter_week_day(str(year), str(quarter),
                                                                    str(project),
                                                                    output_type)
            log_output(query_data)

            day_data = get_per_day_data(query_data)
            project_json['usage_data'] = day_data['usage_data']
            project_json['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        project_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=project_json, status=status)

    return response


'''
    API for getting aggregated cost of each resource for a project for that month
'''


def get_costs_per_resource_week_center(year, week, center, project, output_type):
    log.info(
        'get_costs_per_resource_month_center == {0}--{1} --{2} --{3} -- {4}'.format(year, week, center,
                                                                                    project, output_type))

    project_json = dict()
    usage_data = []
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        resource_list_local = resource_list_per_project(center, project)

        project_json = {
            'usage_data': usage_data,
            'resource_list': resource_list_local,
            'project_list': project_list_local
        }

        if output_type == 'week':
            query_data = get_billing_data_per_resource_week_day_center(str(year), str(week), str(project),
                                                                       output_type)
            log_output(query_data)

            project_json['usage_data'] = get_week_data(query_data, year, None)

        elif output_type == 'day':
            query_data = get_billing_data_per_resource_week_day_center(str(year), str(week), str(project),
                                                                       output_type)
            log_output(query_data)

            day_data = get_per_day_data(query_data)
            project_json['usage_data'] = day_data['usage_data']
            project_json['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        project_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=project_json, status=status)

    return response


'''
    API for getting  cost of a resource for a project for a month
'''


def get_costs_per_resource_per_project_per_day_month(year, value_to_match, center, project, resource, output_type):
    log.info(
        'get_costs_per_resource_per_project_per_day == {0}--{1} --{2} --{3}--{4}--{5} '.format(year, value_to_match,
                                                                                               center, project,
                                                                                               resource, output_type))

    resource_json = dict()
    day_data = dict()
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        resource_list_local = resource_list_per_project(center, project)

        query_data = get_billing_data_per_resource_per_project_per_month(str(year), str(value_to_match),
                                                                         str(project),
                                                                         str(resource), output_type)
        # log_output(query_data)
        log.info(query_data)
        if output_type == 'month' or output_type == 'day':
            day_data = get_per_day_data(query_data)

        elif output_type == 'week':

            day_data['usage_data'] = get_week_data(query_data, year, None)
            day_data['d3_json'] = []

        resource_json = {'usage_data': day_data['usage_data'], 'd3_json': day_data['d3_json'],
                         'project_list': project_list_local,
                         'resource_list': resource_list_local}

    except Exception as e:
        log_error(e[0])
        status = 500
        resource_json['message'] = str(e[0])
        traceback.print_exc()


    response = dict(data=resource_json, status=status)

    return response


'''
    API for getting  cost of a resource for a project for a month
'''


def get_costs_per_resource_per_project_per_day_quarter(year, value_to_match, center, project, resource, output_type):
    log.info('get_costs_per_resource_per_project_per_day_quarter == {0}--{1} --{2} --{3}--{4}--{5} '.format(year,
                                                                                                            value_to_match,
                                                                                                            center,
                                                                                                            project,
                                                                                                            resource,
                                                                                                            output_type))

    resource_json = dict()
    day_data = dict()
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        resource_list_local = resource_list_per_project(center, project)

        query_data = get_billing_data_per_resource_per_project_per_quarter(str(year), str(value_to_match),
                                                                           str(project),
                                                                           str(resource), output_type)
        log_output(query_data)

        if output_type == 'month':
            day_data['usage_data'] = get_per_month_cost(query_data, value_to_match, year)
            day_data['d3_json'] = []
        elif output_type == 'day':
            day_data = get_per_day_data(query_data)
        else:
            day_data['usage_data'] = get_week_data(query_data, year, None)
            day_data['d3_json'] = []

        resource_json = {'usage_data': day_data['usage_data'], 'd3_json': day_data['d3_json'],
                         'project_list': project_list_local,
                         'resource_list': resource_list_local}

    except Exception as e:
        log_error(e[0])
        status = 500
        resource_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=resource_json, status=status)

    return response


'''
    API for getting  cost of a resource for a project for a month
'''


def get_costs_per_resource_per_project_per_day_week(year, value_to_match, center, project, resource, output_type):
    log.info(
        'get_costs_per_resource_per_project_per_day_week == {0}--{1} --{2} --{3}--{4}--{5} '.format(year,
                                                                                                    value_to_match,
                                                                                                    center, project,
                                                                                                    resource,
                                                                                                    output_type))

    resource_json = dict()
    day_data = dict()
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        resource_list_local = resource_list_per_project(center, project)

        query_data = get_billing_data_per_resource_per_project_per_week(str(year), str(value_to_match),
                                                                        str(project),
                                                                        str(resource), output_type)
        log_output(query_data)

        if output_type == 'month' or output_type == 'day':
            day_data = get_per_day_data(query_data)
        else:

            day_data['usage_data'] = get_week_data(query_data, year, None)
            day_data['d3_json'] = []

        resource_json = {'usage_data': day_data['usage_data'], 'd3_json': day_data['d3_json'],
                         'project_list': project_list_local,
                         'resource_list': resource_list_local}

    except Exception as e:
        log_error(e[0])
        status = 500
        resource_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=resource_json, status=status)

    return response


'''
    API for getting  cost of a resource for all project for a month

'''


def get_costs_per_resource_all_project_per_day(year, value_to_match, center, resource, output_type):
    log.info(
        'get_costs_per_resource_all_project_per_day == {0}--{1} --{2} --{3}--{4} '.format(year, value_to_match, center,
                                                                                          resource, output_type))

    resource_json = dict()
    day_data = dict()
    status = 200
    try:
        project_list_local = project_list_per_center(center)['list']
        project_list_ids = project_list_per_center(center)['ids']
        resource_list_local = resource_list_per_project(center, None)

        query_data = get_billing_data_per_resource_all_project_per_day_month(str(year), str(value_to_match),
                                                                             project_list_ids,
                                                                             str(resource), output_type)
        log_output(query_data)

        if output_type == 'month' or output_type == 'day':
            day_data = get_per_day_data(query_data)
        elif output_type == 'week':
            day_data['usage_data'] = get_week_data(query_data, year, None)
            day_data['d3_json'] = []

        resource_json = {'usage_data': day_data['usage_data'], 'd3_json': day_data['d3_json'],
                         'project_list': project_list_local,
                         'resource_list': resource_list_local}
    except Exception as e:
        log_error(e[0])
        status = 500
        resource_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=resource_json, status=status)

    return response


'''
    API for getting  cost of a resource for all project for a month

'''


def get_costs_per_resource_all_project_per_day_quarter(year, value_to_match, center, resource, output_type):
    log.info(
        'get_costs_per_resource_all_project_per_day_quarter == {0}--{1} --{2} --{3}--{4} '.format(year, value_to_match,
                                                                                                  center,
                                                                                                  resource,
                                                                                                  output_type))

    resource_json = dict()
    day_data = dict()
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        project_list_ids = project_list_per_center(center)['ids']
        resource_list_local = resource_list_per_project(center, None)

        query_data = get_billing_data_per_resource_all_project_per_day_quarter(str(year), str(value_to_match),
                                                                               project_list_ids,
                                                                               str(resource), output_type)
        log_output(query_data)

        if output_type == 'month':
            day_data['usage_data'] = get_per_month_cost(query_data, value_to_match, year)
            day_data['d3_json'] = []
        elif output_type == 'day':
            day_data = get_per_day_data(query_data)
        elif output_type == 'week':
            day_data['usage_data'] = get_week_data(query_data, year, None)
            day_data['d3_json'] = []

        resource_json = {'usage_data': day_data['usage_data'], 'd3_json': day_data['d3_json'],
                         'project_list': project_list_local,
                         'resource_list': resource_list_local}
    except Exception as e:
        log_error(e[0])
        status = 500
        resource_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=resource_json, status=status)

    return response


'''
    API for getting  cost of a resource for all project for a month

'''


def get_costs_per_resource_all_project_per_day_week(year, week, center, resource, output_type):
    log.info('get_costs_per_resource_all_project_per_day_week == {0}--{1} --{2} --{3}--{4} '.format(year, week, center,
                                                                                                    resource,
                                                                                                    output_type))
    resource_json = dict()
    day_data = dict()
    status = 200

    try:
        project_list_local = project_list_per_center(center)['list']
        project_list_ids = project_list_per_center(center)['ids']
        resource_list_local = resource_list_per_project(center, None)

        query_data = get_billing_data_per_resource_all_project_per_day_week(str(year), str(week), project_list_ids,
                                                                            str(resource), output_type)
        log_output(query_data)

        if output_type == 'day':
            day_data = get_per_day_data(query_data)
        elif output_type == 'week':
            day_data['usage_data'] = get_week_data(query_data, year, None)
            day_data['d3_json'] = []

        resource_json = {'usage_data': day_data['usage_data'], 'd3_json': day_data['d3_json'],
                         'project_list': project_list_local,
                         'resource_list': resource_list_local}

    except Exception as e:
        log_error(e[0])
        status = 500
        resource_json['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=resource_json, status=status)

    return response


'''
    get cost_center data
'''

'''
    function to get the cost_center list
'''


def get_center_list(unique):
    log_output('in get center list ------')

    cost_center_list = []

    if unique:
        center_list = get_cost_centers(unique)
        log_output(center_list)

        for (cost_center) in center_list:
            cost_center_list.append(cost_center[0])
        if 'other' not in cost_center_list:
            cost_center_list.append('other')
    else:
        cost_center_list = set_global_cost_center_list()
    return cost_center_list


'''
     for getting aggregated cost of each cost center  for that year by quarter
'''


def get_costs_per_center_year_quarter(year, quarter, center, output_type):
    log.info('get_costs_per_center_year_quarter == {0}--{1} --{2} --{3} '.format(year, center, quarter,
                                                                                 output_type))

    data = dict()
    usage_data = []
    status = 200

    log.info('get_costs_per_CENTER_YEAR_quarter == {0} --{1}'.format(year, center))
    try:
        project_list_local = project_list_per_center(center)['list']
        project_ids = project_list_per_center(center)['ids']
        resource_list_local = resource_list_per_project(center, None)

        query_data = get_billing_data_per_year_per_center_quarter(str(year), project_ids, str(quarter),
                                                                  output_type)
        log_output(query_data)
        data = {
            'usage_data': usage_data,
            'project_list': project_list_local,
            'resource_list': resource_list_local
        }
        if output_type == 'month':
            usage_data = get_per_month_cost(query_data, quarter, year)
            data['usage_data'] = usage_data
        elif output_type == 'week':
            usage_data = get_week_data(query_data, year, None)
            data['usage_data'] = usage_data
        elif output_type == 'day':
            day_data = get_per_day_data(query_data)
            data['usage_data'] = day_data['usage_data']
            data['d3_json'] = day_data['d3_json']

    except Exception as e:
        log_error(e[0])
        status = 500
        data['message'] = str(e[0])
        traceback.print_exc()

    response = dict(data=data, status=status)

    return response


def table_create():
    return create_table()


def get_project_by_id(project_id):
    return get_project(project_id)


def update_project_data(cost_center, project_id, project_name, owner, owner_email, contact_name, contact_email,
                        alert_amount):
    if alert_amount == 'none':
        alert_amount = 0
    return update_project(cost_center, project_id, project_name, owner, owner_email, contact_name, contact_email,
                          alert_amount)


def create_project_data(cost_center, project_id, project_name, owner, owner_email, contact_name, contact_email,
                        alert_amount):
    if alert_amount == 'none':
        alert_amount = 0
    return create_project(cost_center, project_id, project_name, owner, owner_email, contact_name, contact_email,
                          alert_amount)


def delete_project_by_id(project_id):
    return delete_project(project_id)
