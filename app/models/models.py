from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_login(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    #backref='author' adds column to post model 
    question = db.relationship('Question', backref='author', lazy=True)
    answer = db.relationship('Answer', backref='author', lazy=True)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.name}', '{self.username}', '{self.email}', '{self.password}')"


class Question(db.Model):
    #tables names are automatically set as the class name with lower case
    question_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    #user.user_id -> referencing the table name and column name. NOT CLASS
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    answer_id = db.relationship('Answer', backref='question', lazy=True)

    def __repr__(self):
        return f"Question ('{self.title}', '{self.date}','{self.content}')"

class Answer(db.Model):
    #tables names are automatically set as the class name with lower case
    answer_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    #user.user_id -> referencing the table name and column name. NOT CLASS
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)


    def __repr__(self):
        return f"Question ('{self.date}','{self.content}')"

db.create_all()
db.session.commit()