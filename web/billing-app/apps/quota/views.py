from apps.billing.billingData import get_center_list
from apps.quota.quotaData import regions_list

__author__ = "Ashwini Chandrasekar(@sriniash)"
__email__ = "ASHWINI_CHANDRASEKAR@homedepot.com"
__version__ = "1.0"
__doc__ = "Billing View API/HTML layer"

from flask import Blueprint, request
from flask.templating import render_template
from flask.wrappers import Response
from apps.config.apps_config import log

import json


mod = Blueprint('quota', __name__, url_prefix='/quota')


'''
    QUOTA PAGE LANDING PAGE
'''
# route handles for /admin and /admin/page
@mod.route('/')
def quota():
    url = 'quota/index.html'
    return render_template(url, title="Cloud Admin Tool")




'''

    API to get the list of regions per  project

'''


@mod.route('/<string:project>', methods=['GET'])
def get_regions_list(project):
    data = dict(data=[], status=200)
    project_list_local = dict()

    cost_center_list = get_center_list(False)
    for project_info in cost_center_list:
        project_list_local[project_info['project_id']] = project_info['project_name']

    for project_id in project_list_local:
        if project_list_local[project_id] == project:
            if 'ID' in project_id:
                project = project_id.split('-')[1]
            else:
                log.info('No ID')
                log.info(project_id)
                project = ''


    data = regions_list(project)

    resp = Response(response=json.dumps(data['data']),
                    status=data['status'],
                    mimetype="application/json")
    return resp
