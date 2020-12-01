from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous.url_safe import URLSafeTimedSerializer
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_pyfile('config.py')
 
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'user_blp.logIn'
login_manager.login_message_category = 'danger'

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

from .questions.routes import questions_blp
from .users.routes import user_blp
from .main.routes import home_blp
from .models.models import User, Question, Answer

app.register_blueprint(questions_blp)
app.register_blueprint(user_blp)
app.register_blueprint(home_blp)

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Answer, db.session))

 