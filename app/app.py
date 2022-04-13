# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from flask_login import login_required, current_user
from flask import render_template, request, jsonify, redirect, url_for
from app import app, db, login_manager
from datetime import datetime
from mongoengine import *

# Register Blueprint so we can factor routes

from auth import auth
from upload import upload, Upload
from staycation import staycation, Staycation
from booking import booking, Booking


# register blueprint from respective module
app.register_blueprint(auth)
app.register_blueprint(upload)
app.register_blueprint(staycation)
app.register_blueprint(booking)

from users import User

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@app.route('/base')
def show_base():
    return render_template('base.html')


@app.route('/packages')
@login_required
def packages():
    staycations = Staycation.objects()

    return render_template('packages.html', name=current_user.name, panel="Package", id='specialCard', staycayList=staycations)

@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template("upload.html", name=current_user.name, panel="Upload")
    elif request.method == 'POST':
        #get values needed
        type = request.form.get('type')
        dataType= request.form.get('dataType')
        if type == 'upload':
            # get the file uploaded, convert CSV to list of Dict, store as a collection, save Staycation objects using the list.
            print('Creating new collection...')
            file = request.files.get('file')
            print('Getting uploads')
            package = Upload(uploads=None).save()
            listOfDict = package.getDictFromCSV(file)
            print('converting csv to dict: ' ,  listOfDict)
            
            if dataType == 'staycation':
                #save all staycations into db
                package.insertIntoStaycationDB(listOfDict)
                for item in listOfDict:
                    Staycation(**item).save()
                print('Staycations saved')
                
            elif dataType == 'users':
                package.insertIntoUserDB(listOfDict)
                for item in listOfDict:
                    User(**item).save()
                print('users saved')
                #Users implementation
            elif dataType == 'booking':
                package.insertIntoBookingDB(listOfDict)
                for item in listOfDict:
                    Booking(**item).save()
                print('Bookings saved')
                #Booking implementation
        return render_template("upload.html", name=current_user.name, panel="Upload")


@app.route("/booking", methods=['GET'])
@app.route("/booking/<hotelId>", methods=['GET', 'POST'])
@login_required
def booking(hotelId):
    #Get the staycation using hotel_name
    currentStaycay = Staycation.objects(id=hotelId)
    
    if request.method == 'GET':
        print('Getting booking template for: ' + hotelId)
        return render_template("booking.html", name=current_user.name, panel="Booking", id='specialCard', staycayObj=currentStaycay, hotelId=hotelId)
    elif request.method == 'POST':
        print('Creating new Booking for ', current_user.name)
        #implement saving of booking here
        dateForm = request.form['bookingDatePicker']
    
        # get proper date to store
        newDate = datetime.strptime(dateForm, "%Y-%m-%d")
        for i in currentStaycay:
            hotelName = i.hotel_name
        #Create new booking
        newBooking = Booking(customer=current_user.email, check_in_date=newDate, hotel_name=hotelName )
        newBooking.save()
        
        
        return redirect(url_for('packages'))
    
@app.route("/getDashboard", methods=['GET'])
@login_required
def loadDashboard():

    #Get all booking objects in specified date range
    print('Getting Booking objects...')
    kwargs = {}
    start = datetime(2022, 1, 17)
    end = datetime(2022, 3, 12)
    raw_query = {'check_in_date': {'$gte': start, '$lte':end}}
    #Getting data for x-axis
    chartObjects = Booking.objects(__raw__=raw_query)
    xAxisObj = []
    xAxis = []
    for i in chartObjects:
        xAxisObj.append(i.check_in_date)
    xAxisObj = sorted(xAxisObj)
    for i in xAxisObj:
        xAxis.append(i.strftime("%Y-%m-%d"))
    
    
    hotelObj = Staycation.objects()
    baseCost = Staycation.objects.distinct('unit_cost')
    hotelNames = Staycation.objects.distinct('hotel_name')
    
    staycationPrices = {}
    for i in range(len(baseCost)):
        staycationPrices[hotelNames[i]] = baseCost[i]
    
    #get unique dates
    uniqueDates32 = []
    for i in xAxis:
        if i not in uniqueDates32:
            uniqueDates32.append(i)
    #count prices
    finalNestedList = []
    for i in hotelObj:
        priceList = countTotalPrice(uniqueDates32, i.hotel_name, i.unit_cost)
        finalNestedList.append(priceList)
    
    print('Sending data to frontend...')
    return jsonify({'labels': hotelNames, 'bookings':chartObjects, 'xAxis':uniqueDates32, 'prices':finalNestedList})
    
@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    print('Rendering Dashboard...')
    return render_template('dashboard.html',name=current_user.name, panel="Dashboard")





#function to get list of prices of a hotel
def countTotalPrice(listOfUniqueDates, hotelName, price):
    # one list of prices must have 17 values
    # one list is for one hotel_name (total 6 lists)
    
    # query for dates involved using hotel name
    listOfActualDatesByHotel = []
    actualDates = Booking.objects(hotel_name = hotelName)
    for i in actualDates:
        listOfActualDatesByHotel.append(i.check_in_date.strftime("%Y-%m-%d"))
    
    hotelList = []
    for i in listOfUniqueDates:
        currentList = []
        currentList = [date for date in listOfActualDatesByHotel if date == i]
        lengthOfList = len(currentList)
        # print(lengthOfList)
        totalPriceForI = lengthOfList * price
        hotelList.append(totalPriceForI)
    
    return hotelList