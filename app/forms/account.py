
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError, Optional
from app.models.models import User

email_reg = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
password_reg = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

class Account_Form(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    username = StringField('Username', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Regexp(email_reg)])
    current_password = PasswordField('Password', validators=[Optional()])
    new_password = PasswordField('Password', validators=[Optional(), Regexp(password_reg), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[Optional(), EqualTo('new_password')])
    submit = SubmitField('Update Account')
    
    
    def validate_username (self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError ("Username in use. Please choose another one.")

    def validate_email (self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError ("Email in use. Log in instead.")


class AccountUnconfirmed_Form(FlaskForm):
    submit = SubmitField('Resed Email')
