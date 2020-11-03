from flask import render_template, url_for, flash, redirect
#same as app.models
from .forms.logIn import Login_Form
from .forms.register import registration_Form 
from app import app, db, bcrypt
from .models.models import User, Question, Answer

@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = Login_Form()

    return render_template('home.html', form2=login_form)

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    form = registration_Form()
    login_form = Login_Form()

    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()


        #message confirming validation success after submiting
        flash(f'Your registration was successful, {form.name.data}', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form, form2=login_form)

