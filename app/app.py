

import json
from flask_login import login_required, current_user
from flask import render_template, request, jsonify, redirect, url_for
from app import app, db, login_manager
from datetime import datetime
from mongoengine import *
import csv
import io


from auth import auth
from staycation import  STAYCATION
from book import Booking
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
    staycations = STAYCATION.objects()

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
            # get the file uploaded, convert CSV to list of Dict
            print('converting csv to dict')
            file = request.files.get('file')
            data = file.read().decode('utf-8')
            dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
            file.close()
            if dataType == 'staycation':
                #save all staycations into db
                for item in dict_reader:
                    newStaycaytion = STAYCATION()
                    newStaycaytion.saveFileToDB(item)
                print('Staycations saved')
            elif dataType == 'users':
                #save all users into db
                for item in dict_reader:
                    newUser = User()
                    newUser.saveFileToDB(item)
                print('users saved')
                #Users implementation
            elif dataType == 'booking':
                #save all bookings into db
                for item in dict_reader:
                    newBooking = Booking()
                    newBooking.saveFileToDB(item)
                print('Bookings saved')
                #Booking implementation
        return render_template("upload.html", name=current_user.name, panel="Upload")


@app.route("/booking", methods=['GET'])
@app.route("/booking/<hotelId>", methods=['GET', 'POST'])
@login_required
def booking(hotelId):
    #Get the staycation using hoteliDs
    currentStaycay = STAYCATION.objects(id=hotelId)
    
    if request.method == 'GET':
        print('Getting booking template for: ' + hotelId)
        return render_template("booking.html", name=current_user.name, panel="Booking", id='specialCard', staycayObj=currentStaycay, hotelId=hotelId)
    elif request.method == 'POST':
        print('Creating new Booking for ', current_user.name)
        #implement saving of booking here
        #Get date, customer email adn hotelname from frontend
        dateForm = request.form['bookingDatePicker']
        customer = current_user.email
        for i in currentStaycay:
            hotelName = i.hotel_name
        #Create new booking
        newBooking = Booking()
        print(f'date: {dateForm} customer email: {customer} hotelName: {hotelName}')
        newBooking.saveOneBookingToDB(dateForm, customer, hotelName)
        
        
        return redirect(url_for('packages'))
    
@app.route("/getDashboard", methods=['GET'])
@login_required
def loadDashboard():

    #Get all booking objects
    print('Getting Booking objects...')
    chartObjects = Booking.objects()
    hotelNames = STAYCATION.objects.distinct('hotel_name')
    for i in chartObjects:
        pass
    
    
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
    hotelObj = STAYCATION.objects()
    baseCost = STAYCATION.objects.distinct('unit_cost')
    # hotelNames = STAYCATION.objects.distinct('hotel_name') 
    
    
    
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
    
    #Saving chart data
    chartResponse = json.dumps({'labels': hotelNames,'xAxis':uniqueDates, 'prices':finalNestedList})
    chartJSON = json.loads(chartResponse)
    Chart(chartObject=chartJSON).save()
    
    print('Sending data to frontend...')
    #Return json object to endpoint
    return jsonify({'labels': hotelNames, 'xAxis':uniqueDates, 'prices':finalNestedList})
    
@app.route("/trendChart/totalIncome", methods=['GET'])
@login_required
def trendChart():
    print('Rendering Total Income...')
    return render_template('trend_chart.html',name=current_user.name, panel="Dashboard", id='trendChart')

@app.route("/trendChart/userDue", methods=['GET'])
def userDue():
    print('Rendering Due Per User...')
    userObject = User.objects()
    return render_template('trend_chart.html',name=current_user.name, panel="Dashboard", id='userDue', userObject=userObject)

@app.route("/trendChart/hotelDue", methods=['GET'])
def hotelDue():
    print('Rendering Due Per Hotel...')
    hotelObject = STAYCATION.objects()
    return render_template('trend_chart.html',name=current_user.name, panel="Dashboard", id='hotelDue', hotelObject=hotelObject)

#function to get list of prices of a hotel
def countTotalPrice(listOfUniqueDates, hotelName, price):
    
    # one list is for one hotel_name (total 6 lists)
    
    # query for dates involved using hotel name
    listOfActualDatesByHotelStr = []
    actualDates = Booking.objects(hotel_name = hotelName)
    staycationObj = STAYCATION.objects(hotel_name = hotelName)
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
        #Total price  per day
        totalPriceForI = lengthOfList * price * duration
        hotelList.append(totalPriceForI)
        #convert all 0 values to 'n/a'
        for i in range(len(hotelList)):
            hotelList[i] = str(hotelList[i])   
            if hotelList[i] == '0.0':
                hotelList[i] = 'n/a' 
    return hotelList


