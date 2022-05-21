from app import db
from flask_login import UserMixin
import csv
import io

class User(UserMixin, db.Document):
    meta = {'collection': 'appUsers'} 
    email = db.StringField(max_length=30) 
    password = db.StringField()
    name = db.StringField()
    
    def saveFileToDB(self, object):
        print(object)
        self.email = object['email']
        self.password = object['password']
        self.name = object['name']
        return self.save()