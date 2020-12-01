from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app.users.token_email import send_email 

from app.users.forms.account import Account_Form, AccountUnconfirmed_Form
from app.users.forms.passwordReset import ResetPassword_Form
from app.users.forms.password import ForgotPassword_Form 
from app.users.forms.register import Registration_Form 
from app.users.forms.activation import Activation_Form
from app.users.forms.logIn import Login_Form

from app.models.models import User, Question, Answer
from app import app, db, bcrypt, mail, s

user_blp = Blueprint("user_blp", __name__)

@user_blp.route('/register', methods=['GET', 'POST'])
def register_route():
    form = Registration_Form()

    if current_user.is_authenticated:
        return redirect(url_for('home_blp.index'))

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

        send_email(email=user.email, 
                        url='user_blp.confirm_email', 
                        subject='Please confirm your email',
                        recipients=[user.email],
                        html='email.html')

    
        flash(f'Activate your account: an email has been sent to {form.email.data}', 'info')
        login_user(user)

    return render_template('auth/register.html', title='Register', form=form)


@user_blp.route('/login', methods=['GET', 'POST'])
def logIn():
    form = Login_Form()

    if current_user.is_authenticated:
        return redirect(url_for('home_blp.index'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You are now loged in, {user.username}', 'success')
        else:
            flash(f'Log in unsuccessful. Please try again', 'danger')

    return render_template('auth/login.html', title='Log In', form=form)


@user_blp.route('/logout')
def logOut():
    logout_user()
    return redirect(url_for('home_blp.index'))


@user_blp.route('/<username>/account', methods=['GET', 'POST'])
@login_required
def account(username):
    form = Account_Form()
    user = User.query.filter_by(username=current_user.username).first()
    
    if current_user.email_confirmation == False:
        flash(f'Activate your account first, {user.name}', 'danger')
        return redirect(url_for('user_blp.unconfirmed', username=user.username))

    if form.validate_on_submit():
        if form.name.data != '':
            user.name = form.name.data
            flash(f'Your account has been updated, {user.name}', 'success')
        
        if form.username.data != '':
            user.username = form.username.data
            flash(f'Your account has been updated, {user.name}', 'success')
        
        if form.email.data != '':
            user.email = form.email.data
            user.email_confirmation = False
            send_email(email=user.email, 
                            url='confirm_email', 
                            subject='Please confirm your email',
                            recipients=[user.email],
                            html='email.html')

            flash(f'Reset Email: a reset link has been sent to your email {form.email.data}', 'success')


        if form.current_password.data or form.new_password.data:
            if form.current_password.data != '' and form.new_password.data != '':
                
                if user and bcrypt.check_password_hash(user.password, form.current_password.data):
                    password_hash = bcrypt.generate_password_hash(form.new_password.data, 14).decode('utf-8')
                    user.password = password_hash
                    flash(f'Your account has been updated, {user.name}', 'success')
                else:
                    flash(f'Your current password is incorrect. Please try again', 'danger')
  
            else:
                flash(f'Both current password and new password must be filled', 'danger')            

        db.session.commit()
            
    return render_template('auth/account.html', title='account', form=form)



@user_blp.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    form = Activation_Form()

    try:
        email = s.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'],max_age=18000)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    user = User.query.filter_by(email=email).first()
    
    if user.email_confirmation:
        flash('Account already confirmed. Please login.', 'info')
    
    else:
        if form.validate_on_submit():
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.email_confirmation = True

                db.session.commit()

                login_user(user)
                flash(f'You have confirmed your account, {user.name} Thanks!', 'success')
            else:
                flash(f'Log in unsuccessful. Please try again', 'danger')

    return render_template('auth/activate.html', title='Account Activation', form=form)



@user_blp.route('/password', methods=['GET', 'POST'])
def password():
    form = ResetPassword_Form()

    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_email(email=form.email.data, 
                            url='user_blp.reset_password', 
                            subject='Reset your password',
                            recipients=[user.email],
                            html='email_password.html')

                flash(f'Reset Password: a reset link has been sent to your email {form.email.data}', 'success')
            else: 
                flash(f"This email doesn't belong to any account. Please register first", 'danger')

    return render_template('auth/reset_password.html', title='Reset Password', form=form)



@user_blp.route('/resetpassword/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ForgotPassword_Form()

    try:
        email = s.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'],max_age=1800)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    user = User.query.filter_by(email=email).first()
    
    if form.validate_on_submit():
        
        password_hash = bcrypt.generate_password_hash(form.password.data, 14).decode('utf-8')
        user.password = password_hash

        db.session.commit()

        login_user(user)
        flash(f'Your password has been changed, {user.name} Thanks!', 'success')
    
    return render_template('auth/password.html', title='Reset Password', form=form)



@user_blp.route('/<username>/unconfirmed', methods=['GET', 'POST'])
@login_required
def unconfirmed(username):
    form = AccountUnconfirmed_Form()

    if current_user.email_confirmation:
        return redirect('/')
    
    if form.validate_on_submit():
        send_email(email=current_user.email, 
                            url='user_blp.confirm_email', 
                            subject='Please confirm your email',
                            recipients=[current_user.email],
                            html='email.html')       
        
        flash(f'Activate your account: an email has been sent to {current_user.email}', 'success')

    return render_template('auth/unconfirmed.html', title='Unconfirmed Account', form=form)



@user_blp.route('/<username>/questions', methods=['GET', 'POST'])
@login_required
def user_questions(username):
    questions = Question.query.filter_by(user_id=current_user.user_id).all()
    questions_count = Question.query.filter_by(user_id=current_user.user_id).count()

    return render_template('auth/user_questions.html', title='Users Questions', questions=questions, questions_count=questions_count)



@user_blp.route('/<username>/answers', methods=['GET', 'POST'])
@login_required
def user_answers(username):
    answers = Answer.query.filter_by(user_id=current_user.user_id).all()
    answers_count = Answer.query.filter_by(user_id=current_user.user_id).count()

    return render_template('auth/user_answers.html', title='Users Answers', answers=answers, answers_count=answers_count)




