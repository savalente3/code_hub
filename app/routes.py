#import packages
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_mail import Message
from app import app, db, bcrypt, mail, s
from flask_login import login_user, current_user, logout_user, login_required

#import forms
#same as app.models
from .forms.logIn import Login_Form
from .forms.register import Registration_Form 
from .forms.account import Account_Form, AccountUnconfirmed_Form
from .forms.activation import Activation_Form
from .forms.password import ForgotPassword_Form 
from .forms.passwordReset import ResetPassword_Form
from .forms.questions import Questions_Form, Anwsers_Form
from .token_email import send_email 

#db
from .models.models import User, Question, Answer

app_blp = Blueprint("user", __name__)

@app.route('/',  methods=['GET', 'POST'])
def index():
    form = Questions_Form()
    
    if form.validate_on_submit():
        questions = Question(title=form.title.data, content=form.content.data, author=current_user)

        db.session.add(questions)
        db.session.commit()

        flash(f'Your Question has been posted, {current_user.username}', 'success')
    
    questions = Question.query.all() 
    return render_template('home.html', form=form, questions=questions)

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    form = Registration_Form()

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

        send_email(email=user.email, 
                            url='confirm_email', 
                            subject='Please confirm your email',
                            recipients=[user.email],
                            html='email.html')

    
        flash(f'Activate your account: an email has been sent to {form.email.data}', 'info')
        login_user(user)

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
    
    if current_user.email_confirmation == False:
        flash(f'Activate your account first, {user.name}', 'danger')
        return redirect(url_for('.unconfirmed', username=user.username))

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
            
    return render_template('account.html', title='account', form=form)



@app.route('/confirm/<token>', methods=['GET', 'POST'])
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

    return render_template('activate.html', title='Account Activation', form=form)



@app.route('/password', methods=['GET', 'POST'])
def password():
    form = ResetPassword_Form()

    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_email(email=form.email.data, 
                            url='reset_password', 
                            subject='Reset your password',
                            recipients=[user.email],
                            html='email_password.html')

                flash(f'Reset Password: a reset link has been sent to your email {form.email.data}', 'success')
            else: 
                flash(f"This email doesn't belong to any account. Please register first", 'danger')

    return render_template('reset_password.html', title='Reset Password', form=form)



@app.route('/resetpassword/<token>', methods=['GET', 'POST'])
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
    

    return render_template('password.html', title='Reset Password', form=form)



@app_blp.route('/<username>/unconfirmed', methods=['GET', 'POST'])
@login_required
def unconfirmed(username):
    form = AccountUnconfirmed_Form()

    if current_user.email_confirmation:
        return redirect('/')
    
    if form.validate_on_submit():
        send_email(email=current_user.email, 
                            url='confirm_email', 
                            subject='Please confirm your email',
                            recipients=[current_user.email],
                            html='email.html')       
        
        flash(f'Activate your account: an email has been sent to {current_user.email}', 'success')

    return render_template('unconfirmed.html', title='Unconfirmed Account', form=form)




@app_blp.route('/questions/<question_id>/', methods=['GET', 'POST'])
def questions(question_id):

    #updates answers
    form2 = Anwsers_Form()  
    #updates question  
    form = Questions_Form()

    
    questions = Question.query.get_or_404(question_id)
    
    if request.method == 'GET':
        form.content.data = questions.content
        form.title.data = questions.title
        
    #edit a question
    if form.validate_on_submit():
        
        if form.content.data != '' or form.title.data != '':
            questions.content = form.content.data
            questions.title = form.title.data
            flash(f'Your question has been edited, {current_user.username}', 'info')
        else:
            db.session.expunge(questions)
    
        
    #post an answer
    if form2.validate_on_submit():
        
        if form2.content_answer.data != '':
            answers = Answer(content=form2.content_answer.data, author=current_user, question=questions)
            answers.content_answer = form2.content_answer.data
            
            form2.content_answer.data = None
            form.content.data = questions.content
            form.title.data = questions.title

            flash(f'Your answer has been posted, {current_user.username}', 'info')     
    
    db.session.commit()

    answers = Answer.query.filter_by(question_id=question_id).all()
    answers_count = Answer.query.filter_by(question_id=question_id).count()
    
    return render_template('questions.html', 
                            title='Your Questions', 
                            questions=questions, 
                            form=form,form2=form2, 
                            answers=answers, 
                            answers_count=answers_count)



@app_blp.route('/<username>/questions', methods=['GET', 'POST'])
@login_required
def user_questions(username):
    questions = Question.query.filter_by(user_id=current_user.user_id).all()
    questions_count = Question.query.filter_by(user_id=current_user.user_id).count()


    return render_template('user_questions.html', title='Users Questions', questions=questions, questions_count=questions_count)



@app_blp.route('/<username>/answers', methods=['GET', 'POST'])
@login_required
def user_answers(username):

    answers = Answer.query.filter_by(user_id=current_user.user_id).all()
    answers_count = Answer.query.filter_by(user_id=current_user.user_id).count()

    return render_template('user_answers.html', title='Users Answers', answers=answers, answers_count=answers_count, questions=questions)
