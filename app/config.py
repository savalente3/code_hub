import os

'''
--------------GET SCRET_KEY--------------
python interpreter -> python on terminal
import secrets
secrets.token_hex(16)
'''


""" 
----------------ENV VARS----------------
-> in proj dir set the env vars on terminal

export SECRET_KEY='the_secret_key'
export SECURITY_PASSWORD_SALT='the_password_salt'

export MAIL_USERNAME='email_username'
export MAIL_PASSWORD='email_password'
export MAIL_DEFAULT_SENDER='full_email' 
"""


"""Base config."""
class Config():
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

 
