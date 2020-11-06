from flask import Flask, render_template, url_for, flash, redirect
#same as app.models
from .forms.logIn import Login_Form
from .forms.register import registration_Form 

from app import app, db, bcrypt
from .models.models import User, Question, Answer


@app.route('/')
def index():

    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    form = registration_Form()
    salt = 14

    if form.validate_on_submit():
        
        password_hash = bcrypt.generate_password_hash(form.password.data, salt).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()

    
        #message confirming validation success after submiting
        flash(f'Your registration was successful, {form.name.data}', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def logIn():
    form = Login_Form()
    return render_template('login.html', title='Log In', form=form)
