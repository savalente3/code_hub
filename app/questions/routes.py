from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_login import current_user, login_required
from app.models.models import Question, Answer
from app.questions.forms.questions import Questions_Form, Anwsers_Form

from app import db

questions_blp = Blueprint("questions_blp", __name__)


@questions_blp.route('/questions/<question_id>/', methods=['GET', 'POST'])
def questions(question_id):

    form2 = Anwsers_Form()  
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
            answers.content = form2.content_answer.data
            
            form2.content_answer.data = None
            form.content.data = questions.content
            form.title.data = questions.title
            
            flash(f'Your answer has been posted, {current_user.username}', 'info')     
    
    db.session.commit()
    answers = Answer.query.filter_by(question_id=question_id).all()
    answers_count = Answer.query.filter_by(question_id=question_id).count()
    
    return render_template('home/questions.html', 
                            title='Your Questions', 
                            questions=questions, 
                            form=form,form2=form2, 
                            answers=answers, 
                            answers_count=answers_count)


@questions_blp.route('/questions/<question_id>/delete_question', methods=['POST'])
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)

    db.session.delete(question)
    db.session.commit()

    flash(f'Your question has been deleted, {current_user.username}', 'danger')     
    return redirect(url_for('home_blp.index'))


@questions_blp.route('/questions/<answer_id>/delete_answer', methods=['POST'])
@login_required
def delete_answer(answer_id):
    answers = Answer.query.get_or_404(answer_id)

    db.session.delete(answers)
    db.session.commit()

    flash(f'Your question has been deleted, {current_user.username}', 'danger')     
    return redirect(f'/questions/{answers.question_id}/')