from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class Questions_Form(FlaskForm):
    title = StringField('Title', validators=[Optional(), Length(max=100)])
    content = TextAreaField('Title', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Post')
