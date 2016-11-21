__author__ = "Ashwini Chandrasekar(@sriniash)"
__email__ = "ASHWINI_CHANDRASEKAR@homedepot.com"
__version__ = "1.0"
__doc__ = "Models relating to the DB tables"

import json

from sqlalchemy.ext.declarative.api import DeclarativeMeta
from apps.config.apps_config import Base

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DATETIME, FLOAT, DECIMAL


'''
   Models :
     Projects Table with : ID, cost_center, project_id,project_name,owner
'''


class Project(Base):
    __tablename__ = 'Project'
    id = Column(Integer, primary_key=True)
    cost_center = Column(String(100))
    project_id = Column(String(16))
    project_name = Column(String(100))
    owner = Column(String(100))
    owner_email = Column(String(100))
    contact_name = Column(String(100))
    contact_email = Column(String(100))
    alert_amount = Column(DECIMAL(12,2))

    def __init__(self, cost_center, project_id, project_name, owner, owner_email, contact_name, contact_email,
                 alert_amount):
        self.cost_center = cost_center
        self.project_id = project_id
        self.project_name = project_name
        self.owner = owner
        self.owner_email = owner_email
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.alert_amount = alert_amount

    def __repr__(self):
        return '<Project %r %r %r %r %r %r %r %r>' % (
            self.cost_center, self.project_id, self.project_name, self.owner, self.owner_email, self.contact_name,
            self.contact_email, self.alert_amount)


'''
  Usage table with : id,usage_date,cost,project_id,resource_type,account_id,usage_value,measurement_unit
  project_id is the reference between this table and Projects table to get the cost center for that project
'''


class Billing(Base):
    __tablename__ = 'Billing'
    id = Column(Integer, primary_key=True)
    usage_date = Column(DATETIME)
    cost = Column(FLOAT)
    project_id = Column(String(16))
    resource_type = Column(String(128))
    account_id = Column(String(24))
    usage_value = Column(DECIMAL(25, 4))
    measurement_unit = Column(String(16))

    def __init__(self, usage_date, cost, project_id, resource_type, account_id, usage_value, measurement_unit):
        self.usage_date = usage_date
        self.cost = cost
        self.project_id = project_id
        self.resource_type = resource_type
        self.account_id = account_id
        self.usage_value = usage_value
        self.measurement_unit = measurement_unit

    def __repr__(self):
        return '<Usage %r %r %r %r %r %r %r >' % (
            self.usage_date, self.cost, self.project_id, self.resource_type, self.account_id, self.usage_value,
            self.measurement_unit)


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
