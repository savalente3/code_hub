from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from app.models.models import User

email_reg = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
password_reg = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
phone_reg = '^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$'

class Registration_Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Regexp(email_reg)])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(phone_reg), Length(min=4, max=16)])
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
    
    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()

        if user:
            raise ValidationError('Phone number in use.')
