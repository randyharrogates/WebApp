from app import db

#class model for booking
class Booking(db.Document):
    meta = {'collection': 'booking'}                                                                                                                                                                                                                                        
    check_in_date = db.DateTimeField()
    customer = db.EmailField()
    hotel_name = db.StringField()
    staycation = db.ReferenceField('staycation')
    