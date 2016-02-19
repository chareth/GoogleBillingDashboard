from apps.billing.billingDBQuery import insert_usage_data

__author__ = 'ashwini'

"""Command-line sample application for listing all objects in a bucket using
the Cloud Storage API.

This sample is used on this page:

    https://cloud.google.com/storage/docs/json_api/v1/json-api-python-samples

For more information, see the README.md under /storage.
"""
import json
from apiclient import discovery
from oauth2client.client import GoogleCredentials
from apps.config.apps_config import BUCKET_NAME, ARCHIVE_BUCKET_NAME, log
import datetime


def data_processor():
    status = 200
    message = 'Prcoess Complete '
    startTime = datetime.datetime.now()
    try:
        bucket = BUCKET_NAME
        archive_bucket = ARCHIVE_BUCKET_NAME

        # Get the application default credentials. When running locally, these are
        # available after running `gcloud init`. When running on compute
        # engine, these are available from the environment.
        credentials = GoogleCredentials.get_application_default()

        # Construct the service object for interacting with the Cloud Storage API -
        # the 'storage' service, at version 'v1'.
        # You can browse other available api services and versions here:
        # https://developers.google.com/api-client-library/python/apis/
        service = discovery.build('storage', 'v1', credentials=credentials)

        # Make a request to buckets.get to retrieve a list of objects in the
        # specified bucket.
        req = service.buckets().get(bucket=bucket)
        resp = req.execute()

        # print(json.dumps(resp, indent=2))

        # Create a request to objects.list to retrieve a list of objects.
        fields_to_return = \
            'nextPageToken,items(name,size,contentType,metadata(my-key))'
        req = service.objects().list(bucket=bucket, fields=fields_to_return)
        file_count = 0

        log.info('Process Start time --- {0}'.format(startTime))
        # If you have too many items to list in one request, list_next() will
        # automatically handle paging with the pageToken.
        while req:
            resp = req.execute()
            # print(json.dumps(resp, indent=2))
            get_filenames(resp, service)
            req = service.objects().list_next(req, resp)


    except Exception as e:
        log.error(' Error in getting Bucket Details - {0}'.format(e[0]))
        message = e[0]
        status = 500

    endTime = datetime.datetime.now()
    log.info('Process End time --- {0}'.format(endTime))
    elapsedTime = startTime - endTime
    time= 'Total Time to Process all the files -- {0}'.format(divmod(elapsedTime.total_seconds(), 60))
    log.info(time)

    response = dict(data=json.dumps(message), status=status, time =time)
    return response


def get_filenames(resp, service):
    try:
        for key, items in resp.iteritems():
            for item in items:
                get_file(item, service)
    except Exception as e:
        log.error('Error in accessing File -- {0}'.format(e[0]))


def get_file(filename, service):
    try:

        log.info('Getting file -- {0}'.format(filename['name']))
        # Get Payload Data
        req = service.objects().get_media(
            bucket=BUCKET_NAME,
            object=filename['name'])
        file_content = req.execute()
        process_file(filename, file_content, service)
    except Exception as e:
        log.error('Error in getting the file -- {0}, {1}'.format(filename['name'], e[0]))


def process_file(filename, file_content, service):
    try:
        log.info('Processing file -- {0} -- STARTING'.format(filename['name']))

        data_list = json.loads(file_content)
        '''
          parse the json and load the data to db
          once loading done move the file to archive folder

          todo : attach timestamp and tmp to file name while processing

        '''
        insert_usage_data(data_list)

        log.info('Processing file -- {0} -- ENDING'.format(filename['name']))

        copy_file_to_archive(filename, service)

    except Exception as e:
        log.error('Error in processing the file -- {0}'.format(e[0]))


def copy_file_to_archive(filename, service):
    try:

        log.info('Starting to move the file to Archive')
        log.info('------------------------------------')

        copy_object = service.objects().copy(sourceBucket=BUCKET_NAME, sourceObject=filename['name'],
                                             destinationBucket=ARCHIVE_BUCKET_NAME, destinationObject=filename['name'],
                                             body={})
        resp = copy_object.execute()

        log.info('Moving of file - {0} to Archive -{1} Done'.format(filename['name'], ARCHIVE_BUCKET_NAME))
        log.info('------------------------------------')

        delete_moved_file(filename, service)

    except Exception as e:

        log.error('Error in Copying the object to archive folder - {0}'.format(e[0]))


def delete_moved_file(filename, service):
    try:
        log.info('Starting to Delete the file  from {0}'.format(BUCKET_NAME))
        log.info('------------------------------------')
        delete_object = service.objects().delete(bucket=BUCKET_NAME, object=filename['name'])
        resp = delete_object.execute()

        log.info('Deleting file - {0}  from - {1} Done'.format(filename['name'], BUCKET_NAME))
        log.info('------------------------------------')

    except Exception as e:
        log.error('Error in deleting the old file - {0}'.format(e[0]))
        # add code to add metadata or rename the file