from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io

staycation = Blueprint('staycation', __name__)

# Document being the csv file uploaded
class Staycation(db.Document):
    meta = {'collection': 'staycation'}
    name = db.StringField()
    duration = db.Duration()
    unitCost = db.IntField()
    URL = db.StringField()
    description = db.StringField()
    
    
    def getDictFromCSV(self, file):
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        file.close()
        return(list(dict_reader))
    
    
    def insertIntoDB(self, data):
        # result = self.insert_many(data) 
        # return result
        
        # fDate = datetime(3000, 1, 1)
        # lDate = datetime(2000, 12, 31)
        # fDate = datetime(3000, 1, 1)
        # lDate = datetime(2000, 12, 31)

        for item in data:
            
            # BMI(name=item['User'], date=myDate, bmi=item['BMI']).save()
            if readings.get(item['User']):
                readings[item['User']].append([item['Date'], item['BMI']])            
            else:
                readings[item['User']] = [[item['Date'], item['BMI']]]
            
        # dbd.readings.insert_one({"readings": readings, "fDate": fDate, "lDate": lDate})
        self.update(__raw__={'$set': {'readings': readings,'fdate': fDate, 'ldate': lDate}})
    
    
