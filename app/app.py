# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from app.staycaytion import Staycation
from flask_login import login_required, current_user
from flask import render_template, request
from app import app, db, login_manager

# Register Blueprint so we can factor routes
# from bmi import bmi, get_dict_from_csv, insert_reading_data_into_database
from bmi import bmi
from dashboard import dashboard, CHART
from auth import auth

# register blueprint from respective module
app.register_blueprint(dashboard)
app.register_blueprint(auth)
app.register_blueprint(bmi)

from users import User

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/base')
def show_base():
    return render_template('base.html')

@app.route('/packages')
def log():
    return render_template('packages.html', name=current_user.name, panel="Packages", id='specialCard')

@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template("upload.html", name=current_user.name, panel="Upload")
    elif request.method == 'POST':
        type = request.form.get('type')
        if type == 'create':
            print("No create Action yet")
        elif type == 'upload':
            file = request.files.get('file')
            staycayPack = Staycation(uploads=None).save()
            listOfDict = staycayPack.getDictFromCSV(file)
            staycayPack.insertIntoDB(listOfDict)
        return render_template("upload.html", name=current_user.name, panel="Upload")
    
