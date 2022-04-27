# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from flask_login import login_required, current_user
from flask import render_template, request, jsonify, redirect, url_for
from app import app, db, login_manager
from datetime import datetime
from mongoengine import *


from auth import auth
from upload import Upload
from staycation import  Staycation
from booking import Booking
from users import User

#Register blueprint for auth for login, logout and register
app.register_blueprint(auth)


#To handle login and load current user
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

#To render base template
@app.route('/base')
def show_base():
    return render_template('base.html')

#to render staycation packages
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
            # get the file uploaded, convert CSV to list of Dict, store as a collection for all uploads
            print('Creating new collection...')
            file = request.files.get('file')
            print('Getting uploads')
            package = Upload(uploads=None).save()
            listOfDict = package.getDictFromCSV(file)
            print('converting csv to dict: ' ,  listOfDict)
            
            if dataType == 'staycation':
                #save all staycations into db
                for item in listOfDict:
                    Staycation(**item).save()
                print('Staycations saved')
                
            elif dataType == 'users':
                #save all users into db
                for item in listOfDict:
                    User(**item).save()
                print('users saved')
                #Users implementation
            elif dataType == 'booking':
                #save all bookings into db
                for item in listOfDict:
                    Booking(**item).save()
                print('Bookings saved')
                #Booking implementation
        return render_template("upload.html", name=current_user.name, panel="Upload")


@app.route("/booking", methods=['GET'])
@app.route("/booking/<hotelId>", methods=['GET', 'POST'])
@login_required
def booking(hotelId):
    #Get the staycation using hoteliDs
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

    #Get all booking objects
    print('Getting Booking objects...')
    chartObjects = Booking.objects()
    xAxisObj = []
    xAxis = []
    #Get dates
    for i in chartObjects:
        xAxisObj.append(i.check_in_date)
    #sort dates
    #dates is in datetimeformat
    xAxisObj = sorted(xAxisObj)
    #convert dates to string
    #dates is in string format
    for i in xAxisObj:
        xAxis.append(i.strftime("%Y-%m-%d"))
    
    #get all relavant objects
    hotelObj = Staycation.objects()
    baseCost = Staycation.objects.distinct('unit_cost')
    hotelNames = Staycation.objects.distinct('hotel_name') 
    
    
    
    #get unique dates
    uniqueDates = []
    for i in xAxis:
        if i not in uniqueDates:
            uniqueDates.append(i)
    #count prices for all 6 hotels
    finalNestedList = []
    for i in hotelObj:
        priceList = countTotalPrice(uniqueDates, i.hotel_name, i.unit_cost)
        finalNestedList.append(priceList)
    
    print('Sending data to frontend...')
    #Return json object to endpoint
    return jsonify({'labels': hotelNames, 'bookings':chartObjects, 'xAxis':uniqueDates, 'prices':finalNestedList})
    
@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    print('Rendering Dashboard...')
    return render_template('dashboard.html',name=current_user.name, panel="Dashboard")





#function to get list of prices of a hotel
def countTotalPrice(listOfUniqueDates, hotelName, price):
    
    # one list is for one hotel_name (total 6 lists)
    
    # query for dates involved using hotel name
    listOfActualDatesByHotelStr = []
    actualDates = Booking.objects(hotel_name = hotelName)
    staycationObj = Staycation.objects(hotel_name = hotelName)
    #Get the particular duration of hotel involved
    duration = 0
    for i in staycationObj:
        duration += int(i.duration)
    #get the actual booking dates of the hotel involved
    actualDatesList = []
    for i in actualDates:
        actualDatesList.append(i.check_in_date)
    #Add in more dates according to duration
    
    #Conver to string
    for i in actualDatesList:
        listOfActualDatesByHotelStr.append(i.strftime("%Y-%m-%d"))
    
    #Do a for loop to get a the list of values
    hotelList = []
    for i in listOfUniqueDates:
        currentList = []
        currentList = [date for date in listOfActualDatesByHotelStr if date == i]
        lengthOfList = len(currentList)
        print(lengthOfList)
        #Total price  per day
        totalPriceForI = lengthOfList * price * duration
        hotelList.append(totalPriceForI)
        #convert all 0 values to 'n/a'
        for i in range(len(hotelList)):
            hotelList[i] = str(hotelList[i])   
            if hotelList[i] == '0.0':
                hotelList[i] = 'n/a' 
    return hotelList


