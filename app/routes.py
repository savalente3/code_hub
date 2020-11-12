from flask import Flask, render_template, url_for, flash, redirect
#same as app.models
from .forms.logIn import Login_Form
from .forms.register import registration_Form 
from .forms.account import account_Form 
from flask_login import login_user, current_user, logout_user

from app import app, db, bcrypt
from .models.models import User, Question, Answer


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    form = registration_Form()
    salt = 14

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():

        password_hash = bcrypt.generate_password_hash(form.password.data, salt).decode('utf-8')

        user = User(name=form.name.data, username=form.username.data, email=form.email.data, phone=form.phone.data, password=password_hash)
        db.session.add(user)
        db.session.commit()

    
        #message confirming validation success after submiting
        flash(f'Your registration was successful, {form.name.data}', 'success')
        return redirect(url_for('register_route'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def logIn():
    form = Login_Form()

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You are now loged in, {user.username}', 'success')
        else:
            flash(f'Log in unsuccessful. Please try again', 'danger')

    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logOut():
    logout_user()
    return redirect(url_for('index'))



@app.route('/account', methods=['GET', 'POST'])
def account():
    form = account_Form()
    return render_template('account.html', title='Your Account', form=form)
