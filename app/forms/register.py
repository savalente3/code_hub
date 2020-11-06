from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from app.models.models import User

email_reg = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
password_reg = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

class registration_Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Regexp(email_reg)])
    password = PasswordField('Password', validators=[DataRequired(), Regexp(password_reg), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password') ])
    submit = SubmitField('Create Account')

    def validate_username (self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError ("Username in use. Please choose another one.")

    def validate_email (self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError ("Email in use. Log in instead.")
