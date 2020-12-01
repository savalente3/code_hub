from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.config import Config


 
db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'user_blp.logIn'
login_manager.login_message_category = 'danger'

mail = Mail()

def Create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from .questions.routes import questions_blp
    from .users.routes import user_blp
    from .main.routes import home_blp

    app.register_blueprint(questions_blp)
    app.register_blueprint(user_blp)
    app.register_blueprint(home_blp)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    
    with app.app_context():
        db.create_all()
        db.session.commit()
    
    return app
    

from app.models.models import User, Question, Answer

admin = Admin()
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Answer, db.session))