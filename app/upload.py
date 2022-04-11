from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io

upload = Blueprint('upload', __name__)

# Document being the csv file uploaded
class Upload(db.Document):
    meta = {'collection': 'upload'}
    uploads = db.DictField()                                                                                                                                                                                                                                         
    # hotel_name = db.StringField()
    # duration = db.IntField()
    # unit_cost = db.FloatField()
    # image_url = db.URLField()
    # description = db.StringField()
    
    def getDictFromCSV(self, file):
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        file.close()
        return(list(dict_reader))
    
    
    def insertIntoDB(self, data):
        # result = self.insert_many(data) 
        # return result
        packages = {}
        # fDate = datetime(3000, 1, 1)
        # lDate = datetime(2000, 12, 31)
        # fDate = datetime(3000, 1, 1)
        # lDate = datetime(2000, 12, 31)

        for item in data:
            
            # BMI(name=item['User'], date=myDate, bmi=item['BMI']).save()
            if packages.get(item['hotel_name']):
                packages[item['hotel_name']].append([item['duration'], item['unit_cost'], item['image_url'], item['description']])
            else:
                packages[item['hotel_name']] = [[item['duration'], item['unit_cost'], item['image_url'], item['description']]]
        # dbd.readings.insert_one({"readings": readings, "fDate": fDate, "lDate": lDate})
        self.update(__raw__={'$set': {'uploads': packages}})
    

    
