from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../config.py')
from app import routes

db = SQLAlchemy(app)
from .models.models import User, Question, Answer