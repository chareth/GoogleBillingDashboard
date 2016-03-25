__author__ = 'ashwini'

import json
from apiclient import discovery
from oauth2client.client import GoogleCredentials

from apps.config.apps_config import log


def regions_list(id):
    data =[]
    items_list =[]
    status = 200
    print id
    try:

        # Get the application default credentials. When running locally, these are
        # available after running `gcloud init`. When running on compute
        # engine, these are available from the environment.
        credentials = GoogleCredentials.get_application_default()

        # Construct the service object for interacting with the Cloud Storage API -
        # the 'storage' service, at version 'v1'.
        # You can browse other available api services and versions here:
        # https://developers.google.com/api-client-library/python/apis/
        service = discovery.build('compute', 'v1', credentials=credentials)

        # Create a request to objects.list to retrieve a list of objects.
        fields_to_return = \
            'nextPageToken,items(name,size,contentType,metadata(my-key))'
        req = service.regions().list(project=id)

        # If you have too many items to list in one request, list_next() will
        # automatically handle paging with the pageToken.

        while req:
            resp = req.execute()
            data.append(resp)
            #print(json.dumps(resp, indent=2))
            req = service.regions().list_next(req, resp)

        for datas in data:
            items_list += datas['items']



    except Exception as e:
        log.error(' Error in getting Bucket Details - {0}'.format(e[0]))
        message = e[0]
        status = 500

    response = dict(data=items_list, status=status)
    return response

