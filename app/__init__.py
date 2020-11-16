from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import current_user


app = Flask(__name__)
app.config.from_pyfile('../config.py')
 
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'logIn'
login_manager.login_message_category = 'danger'


from app import routes
from .routes import app_blp

app.register_blueprint(app_blp)
