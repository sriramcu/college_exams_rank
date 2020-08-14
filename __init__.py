from flask import Flask
#import config
#from config import Config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////home/sriram/work/rvcesqlresults/sql_new_sem1results18.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from rvce_web_results import routes, models
