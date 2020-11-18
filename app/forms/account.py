
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError, Optional
from app.models.models import User

email_reg = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
password_reg = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

class Account_Form(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    username = StringField('Username', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Regexp(email_reg)])
    submit = SubmitField('Update Account')

    def validate_username (self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError ("Username in use. Please choose another one.")

    def validate_email (self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError ("Email in use. Log in instead.")
