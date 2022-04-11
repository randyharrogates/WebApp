from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta, date
from flask_login import current_user
from app import db

import csv
import io
import math

bmi = Blueprint('bmi', __name__)
class BMILOG(db.Document):
    meta = {'collection': 'bmilog'}
    name = db.StringField(max_length=30)
    datetime = db.DateTimeField()
    weight = db.FloatField()
    height = db.FloatField()
    bmi = db.FloatField()
    def computeBMI(self, unit):
        if unit == 'm':
            bmi = self.weight / math.pow(self.height, 2)
        else:
            bmi = self.weight / math.pow(self.height/100, 2)
        return bmi

class BMIDAILY(db.Document):
    
    meta = {'collection': 'bmidaily'}
    name = db.StringField(max_length=30)
    date = db.DateTimeField()
    numberOfMeasures = db.IntField()
    averageBMI = db.FloatField()
    
    def updatedBMI(self, newBMI):
        return (newBMI + (self.averageBMI * self.numberOfMeasures)) / (self.numberOfMeasures + 1) 

 
@bmi.route('/process',methods= ['POST'])
def process():
    weight  = float(request.form['weight'])
    height = float(request.form['height'])

    # Since there is only one reading allowed in each day, the latest will be the log
    today = date.today()
    now = datetime.now()
    
    bmilogObject = BMILOG(name=current_user.name, datetime=now, weight=weight, height=height)
    bmilogObject.bmi = bmilogObject.computeBMI(request.form['unit'])
    bmilogObject.save()
    
    bmidailyObjects = BMIDAILY.objects(name=current_user.name, date=today)
    
    if len(bmidailyObjects) >= 1:
        new_bmi_average = bmidailyObjects[0].updatedBMI(bmilogObject.bmi)
        number = bmidailyObjects[0].numberOfMeasures
        #.update (include save) 
        bmidailyObjects[0].update(__raw__={'$set': {'numberOfMeasures': number + 1, 'averageBMI': new_bmi_average}})
    else:
        bmidailyObject = BMIDAILY(name=current_user.name, date=today, numberOfMeasures=1, averageBMI = bmilogObject.bmi)
        bmidailyObject.save()

    # Paul
    #bryan
    return jsonify({'bmi' : bmilogObject.bmi})
