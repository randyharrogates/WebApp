from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db
import datetime
import csv
import io

booking = Blueprint('booking', __name__)

#class model for booking
class Booking(db.Document):
    meta = {'collection': 'booking'}                                                                                                                                                                                                                                        
    check_in_date = db.DateTimeField()
    customer = db.EmailField()
    hotel_name = db.StringField()
    staycation = db.ReferenceField('staycation')
    