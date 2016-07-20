__author__ = "Ashwini Chandrasekar(@sriniash)"
__email__ = "ASHWINI_CHANDRASEKAR@homedepot.com"
__version__ = "1.0"
__doc__ = "Models relating to the DB tables"

import json

from sqlalchemy.ext.declarative.api import DeclarativeMeta
from apps.config.apps_config import Base

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DATETIME, FLOAT, DECIMAL


class Usage(Base):
    __tablename__ = 'usage'
    id = Column(Integer, primary_key=True)
    usage_date = Column(DATETIME)
    resource_type = Column(String(128))
    resource_id = Column(String(128))
    resource_uri = Column(String(100))
    location = Column(String(100))
    usage_value = Column(Integer)
    measurement_unit = Column(String(16))

    def __init__(self, usage_date, resource_type, resource_id, resource_uri, location, usage_value, measurement_unit):
        self.usage_date = usage_date
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.resource_uri = resource_uri
        self.location = location
        self.usage_value = usage_value
        self.measurement_unit = measurement_unit

    def __repr__(self):
        return '<Usage %r %r %r %r %r %r %r >' % (
            self.usage_date, self.resource_type, self.resource_id, self.resource_uri,
            self.location, self.usage_value, self.measurement_unit)


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
