from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io

booking = Blueprint('booking', __name__)

class Booking(db.Document):
    meta = {'collection': 'booking'}
    # uploads = db.DictField()                                                                                                                                                                                                                                         
    check_in_date = db.DateTimeField()
    customer = db.StringField()
    hotel_name = db.StringField()
