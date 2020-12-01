from flask import render_template, flash, Blueprint
from app.models.models import Question
from app.questions.forms.questions import Questions_Form
from flask_login import current_user

from app import db

home_blp = Blueprint("home_blp", __name__)

@home_blp.route('/',  methods=['GET', 'POST'])
def index():
    form = Questions_Form()
    
    if form.validate_on_submit():
        questions = Question(title=form.title.data, content=form.content.data, author=current_user)
        
        if form.content.data != '' or form.title.data != '':
            db.session.add(questions)
            db.session.commit()

        form.title.data = None
        form.content.data = None
        flash(f'Your Question has been posted, {current_user.username}', 'info')
    
    questions = Question.query.all() 
    return render_template('home/home.html', form=form, questions=questions)


