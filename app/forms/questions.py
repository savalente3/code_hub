from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


class Questions_Form(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=1000)])
    content = TextAreaField('Question', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Post')

class Anwsers_Form(FlaskForm):
    content_answer = TextAreaField('Question', validators=[Optional(), Length(max=2000)])
    submit_answer = SubmitField('Post')
