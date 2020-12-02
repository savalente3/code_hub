from flask import render_template, flash, Blueprint, current_app
from app.models.models import User, Question
from app.questions.forms.questions import Questions_Form
from flask_login import current_user

from app import db, bcrypt

home_blp = Blueprint("home_blp", __name__)

@home_blp.route('/',  methods=['GET', 'POST'])
def index():
    form = Questions_Form()

    if User.query.filter_by(email=current_app.config['SEED_ADMIN_EMAIL']).first() is None:
        password_hash = bcrypt.generate_password_hash(current_app.config['SEED_ADMIN_PASSWORD'], 14).decode('utf-8')
        user = User(name='admin', 
                username='admin', 
                email=current_app.config['SEED_ADMIN_EMAIL'], 
                password=password_hash,
                email_confirmation=True,
                admin=True)

        db.session.add(user)
    else:
        pass
     
    if form.validate_on_submit():
        questions = Question(title=form.title.data, content=form.content.data, author=current_user)
        
        if form.content.data != '' or form.title.data != '':
            db.session.add(questions)

        form.title.data = None
        form.content.data = None
        flash(f'Your Question has been posted, {current_user.username}', 'info')
    
    db.session.commit()
    questions = Question.query.all() 
    return render_template('home/home.html', form=form, questions=questions)


