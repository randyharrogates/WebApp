from users import User
from staycation import STAYCATION
from app import db, app




#class model for booking

class Booking(db.Document):
    meta = {'collection': 'booking'}
    check_in_date = db.DateTimeField(required=True) 
    customer = db.ReferenceField(User)
    package = db.ReferenceField(STAYCATION) 
    total_cost = db.FloatField()
    
    def calculate_total_cost(self):
        self.total_cost = self.package.duration * self.package.unit_cost
        
    def saveFileToDB(self, object):
        self.check_in_date = object['check_in_date']
        self.customer = User.objects.get(email = object['customer'])
        self.package = STAYCATION.objects.get(hotel_name = object['hotel_name'])
        self.calculate_total_cost()
        print(self.total_cost)
        return self.save()

    def saveOneBookingToDB(self, check_in_date, customer, package):
        self.check_in_date = check_in_date
        self.customer = User.objects.get(email = customer)
        self.package = STAYCATION.objects.get(hotel_name = package)
        self.calculate_total_cost()
        print(self.total_cost, self.customer,self.package, self.check_in_date)
        return self.save()  