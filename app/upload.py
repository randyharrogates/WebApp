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
    
    
    def getDictFromCSV(self, file):
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        file.close()
        return(list(dict_reader))
    
    
    def insertIntoStaycationDB(self, data):
        
        packages = {}
        

        for item in data:
            
            if packages.get(item['hotel_name']):
                packages[item['hotel_name']].append([item['duration'], item['unit_cost'], item['image_url'], item['description']])
            else:
                packages[item['hotel_name']] = [[item['duration'], item['unit_cost'], item['image_url'], item['description']]]
        self.update(__raw__={'$set': {'uploads': packages}})
        
    def insertIntoUserDB(self, data):
        packages = {}
        

        for item in data:
            if packages.get(item['name']):
                packages[item['name']].append([item['email'], item['password']])
            else:
                packages[item['name']] = [[item['email'], item['password']]]
        self.update(__raw__={'$set': {'uploads': packages}})
        
    def insertIntoBookingDB(self, data):
        
        packages = {}
        

        for item in data:
            
            if packages.get(item['customer']):
                packages[item['customer']].append([item['check_in_date'], item['hotel_name']])
            else:
                packages[item['customer']] = [[item['check_in_date'], item['hotel_name']]]
        self.update(__raw__={'$set': {'uploads': packages}})
    
    

    





