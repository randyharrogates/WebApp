

from datetime import datetime, timedelta, date
from app import db



#staycation class for staycation packages

class Staycation(db.Document):
    meta = {'collection': 'staycation'}
                                                                                                                                                                                                                                           
    hotel_name = db.StringField()
    duration = db.IntField()
    unit_cost = db.FloatField()
    image_url = db.URLField()
    description = db.StringField()