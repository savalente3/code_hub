from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

password_reg = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'


class Activation_Form(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Activate')

