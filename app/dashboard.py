from app import db

#chart class for chart model

class Chart(db.Document):
    meta = {'collection': 'chart'}                                                                                                                                                                                                                           
    chartObject = db.DictField()
    
    