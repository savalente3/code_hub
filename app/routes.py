from flask import Flask, render_template, url_for, flash, redirect
#same as app.models
from .forms.logIn import Login_Form
from .forms.register import registration_Form 

from app import app


@app.route('/')
def index():

    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    form = registration_Form()

    if form.validate_on_submit():
        #message confirming validation success after submiting
        flash(f'Your registration was successful, {form.name.data}', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def logIn():
    form = Login_Form()
    return render_template('login.html', form=form)
