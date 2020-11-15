from flask import Flask, render_template, url_for, flash, redirect, request
#same as app.models
from .forms.logIn import Login_Form
from .forms.register import Registration_Form 
from .forms.account import Account_Form 
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db, bcrypt
from .models.models import User, Question, Answer


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    form = Registration_Form()
    salt = 14

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():

        password_hash = bcrypt.generate_password_hash(form.password.data, salt).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, phone=form.phone.data, password=password_hash)
        
        #creates new user and adds it to db
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
@login_required
def account():
    form = Account_Form()

    user = User.query.filter_by(username=current_user.username).first()

    if form.validate_on_submit():
        if form.name.data != '':
            user.name = form.name.data
        
        if form.username.data != '':
            user.username = form.username.data
        
        if form.email.data != '':
            user.email = form.email.data
        
        if form.phone.data != '':
            user.phone = form.phone.data

        db.session.commit()
    
        #message confirming validation success after submiting
        flash(f'Your account has been updated, {form.name.data}', 'success')

    return render_template('account.html', title='account', form=form)
