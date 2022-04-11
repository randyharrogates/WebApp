# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from flask_login import login_required, current_user
from flask import render_template, request, jsonify, redirect, url_for
from app import app, db, login_manager

# Register Blueprint so we can factor routes
# from bmi import bmi, get_dict_from_csv, insert_reading_data_into_database
from bmi import bmi
from dashboard import dashboard, CHART
from auth import auth
from upload import upload, Upload
from staycation import staycation, Staycation
from booking import booking, Booking


# register blueprint from respective module
app.register_blueprint(dashboard)
app.register_blueprint(auth)
app.register_blueprint(bmi)
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
def packages():
    staycations = Staycation.objects()
    # print(staycations)
    # for i in staycations:
    #     print(i.hotel_name)

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
            if dataType == 'staycation':
                # get the file uploaded, convert CSV to list of Dict, store as a collection, save Staycation objects using the list.
                print('Creating new collection...')
                file = request.files.get('file')
                print('Getting uploads')
                package = Upload(uploads=None).save()
                listOfDict = package.getDictFromCSV(file)
                print('converting csv to dict: ' ,  listOfDict)
                package.insertIntoDB(listOfDict)
                for item in listOfDict:
                    Staycation(**item).save()
                print('Staycations saved')
                
            elif dataType == 'users':
                pass
                #Users implementation
            elif dataType == 'booking':
                #Booking implementation
                pass
        return render_template("upload.html", name=current_user.name, panel="Upload")


@app.route("/booking", methods=['GET' , 'POST'])
@app.route("/booking/<hotelName>", methods=['GET', 'POST'])
def booking(hotelName=None):
    #Get the staycation using hotel_name
    currentStaycay = Staycation.objects(hotel_name=hotelName)
    
    if request.method == 'GET':
        print('Getting booking template for: ' + hotelName)
        return render_template("booking.html", name=current_user.name, panel="Booking", id='specialCard', staycayObj=currentStaycay, hotelName=hotelName)
    elif request.method == 'POST':
        print('Goes to post')
        #implement saving of booking here
        dateForm = request.form['bookingDatePicker']
        print(dateForm)
        # list in year, month, day
        dateFormList = dateForm.split('-')
        print(dateFormList)
        
        
        return redirect(url_for('packages'))
    
