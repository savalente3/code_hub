from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint
from flask_mail import Message
from app import app, db, bcrypt, mail
from itsdangerous.url_safe import URLSafeTimedSerializer
from flask_login import login_user, current_user, logout_user, login_required

#same as app.models
from .forms.logIn import Login_Form
from .forms.register import Registration_Form 
from .forms.account import Account_Form 

from .models.models import User, Question, Answer

app_blp = Blueprint("user", __name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    form = Registration_Form()
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():

        password_hash = bcrypt.generate_password_hash(form.password.data, 14).decode('utf-8')
        user = User(name=form.name.data, 
                    username=form.username.data, 
                    email=form.email.data, 
                    password=password_hash,
                    email_confirmation=False)
        
        #creates new user and adds it to db
        db.session.add(user)
        db.session.commit()

        
        token = s.dumps(user.email, salt=app.config['SECURITY_PASSWORD_SALT'])
        confirm_url = url_for('confirm_email', token=token, _external=True)
        activate_html = render_template('email.html', confirm_url=confirm_url)
        
        msg = Message("Please confirm your email", 
                    sender="sa.valente3@gmail.com", 
                    recipients=["jijayob934@biiba.com"],
                    html=activate_html)        
        
        print(f"---------------TOKEN: {confirm_url}---------------")
        

        mail.send(msg)

        #message confirming validation success after submiting
        flash(f'Activate your account: an email has been sent to {form.email.data}', 'success')

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


@app_blp.route('/<username>/account', methods=['GET', 'POST'])
@login_required
def account(username):
    form = Account_Form()

    user = User.query.filter_by(username=current_user.username).first()

    if form.validate_on_submit():
        if form.name.data != '':
            user.name = form.name.data
        
        if form.username.data != '':
            user.username = form.username.data
        
        if form.email.data != '':
            user.email = form.email.data

        db.session.commit()
    
        #message confirming validation success after submiting
        flash(f'Your account has been updated, {form.name.data}', 'success')

    return render_template('account.html', title='account', form=form)



@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    try:
        email = s.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'],max_age=18000)
    except:

        flash('The confirmation link is invalid or has expired.', 'danger')

    user = User.query.filter_by(email=email).first()

    if user.email_confirmation:
        flash('Account already confirmed. Please login.', 'info')
    else: 
        user.email_confirmation = True
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        
        flash('You have confirmed your account. Thanks!', 'success')

    return render_template('activate.html', title='Account Activation')