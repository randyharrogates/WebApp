

#staycation class for staycation packages

from app import db
import csv
import io

class STAYCATION(db.Document):
    meta = {'collection': 'staycation'} 
    hotel_name = db.StringField(max_length=30) 
    duration = db.IntField()
    unit_cost = db.FloatField()
    image_url = db.StringField(max_length=30) 
    description = db.StringField(max_length=500)
    
    #Method to convert unit_cost to float so that it can be stored into floatfield
    def doConvertUnitCost(self, object):
        value = object['unit_cost']
        convertedValue = float(value)
        return convertedValue
        
    def saveFileToDB(self, object):
        convertedUnitCost = self.doConvertUnitCost(object)
        self.hotel_name = object['hotel_name']
        self.duration = object['duration']
        self.unit_cost = convertedUnitCost
        self.image_url = object['image_url']
        self.description = object['description']
        return self.save()
    
    