import logging
import os

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.pool import NullPool

from apscheduler.schedulers.background import BackgroundScheduler



scheduler = BackgroundScheduler()
scheduler.start()

file_path = os.path.abspath(os.getcwd()) + "/data/reporting.db"
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
SQLALCHEMY_RECORD_QUERIES = True

'''
  SQL DB

'''
#SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/reporting'
SQLALCHEMY_DATABASE_URI = 'mysql://' + os.environ.get('MYSQL_USER') + ':' + os.environ.get(
    'MYSQL_PASS') + '@' + os.environ.get('MYSQL_HOST') + '/' + os.environ.get('MYSQL_DBNAME')

log = logging.getLogger()

engine = create_engine(SQLALCHEMY_DATABASE_URI, poolclass=NullPool)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

'''
  Data Processor Constants
'''

BUCKET_NAME = os.environ.get('BUCKET_NAME')
ARCHIVE_BUCKET_NAME = os.environ.get('ARCHIVE_BUCKET_NAME')

'''

UnComment out this when running locally in docker  -- add the service account json inside the web/billing-app folder
'''
'''
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/usr/src/app/billing-app/service-account.json"
'''

'''
    query error logging
'''


def log_error(e):
    return log.error('Error -- {0}'.format(e))


'''
    query output logging
'''


def log_output(data):
    return log.info('Data -- {0}'.format(data))


