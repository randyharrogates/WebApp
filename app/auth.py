
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, redirect, render_template, url_for, flash
from forms import RegForm
from users import User
from staycation import Staycation
from booking import Booking

#blueprint defined to use auth.route
auth = Blueprint('auth', __name__)

#Used for register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        #validate if user exists
        if form.validate():
            existingUser = User.objects(email=form.email.data).first()
            #if new user, save the user
            if existingUser is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                newUser = User(email=form.email.data,password=hashpass, name=form.name.data).save()
                login_user(newUser)
                return redirect(url_for('dashboard'))
            #else return error
            else:
                form.email.errors.append("User already existed")
                render_template('register.html', form=form, panel="Register")    
            
    return render_template('register.html', form=form, panel="Register")

#Used for login rendering
@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/')
def login():
    
    form = RegForm()
    if request.method == 'POST':
        print(request.form.get('checkbox'))
        #validate the user
        if form.validate():
            validateUser = User.objects(email=form.email.data).first()
            if validateUser:
                #redirect to packages if user is found
                if check_password_hash(validateUser['password'], form.password.data):
                    login_user(validateUser)
                    return redirect(url_for('packages'))
                else:
                    form.password.errors.append("User Password Not Correct")
            else:
                #else return error msg
                form.email.errors.append("No Such User")
    return render_template('login.html', form=form, panel="Login")

#Used for logout rendering
@auth.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

