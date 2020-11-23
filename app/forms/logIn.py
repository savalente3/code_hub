from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional


class Login_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Optional()])
    submit = SubmitField('Log In')
    remember = BooleanField('Remeber Me')
