from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io

staycation = Blueprint('staycation', __name__)

class Staycation(db.Document):
    meta = {'collection': 'staycation'}
    # uploads = db.DictField()                                                                                                                                                                                                                                         
    hotel_name = db.StringField()
    duration = db.IntField()
    unit_cost = db.FloatField()
    image_url = db.URLField()
    description = db.StringField()