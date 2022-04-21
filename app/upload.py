from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io



# Class model for upload
class Upload(db.Document):
    meta = {'collection': 'upload'}
    uploads = db.DictField()                                                                                                                                                                                                                                         
    
    # Function used to convert the csv file to a list of dict to save into db
    def getDictFromCSV(self, file):
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        file.close()
        return(list(dict_reader))
    
    
    

    





