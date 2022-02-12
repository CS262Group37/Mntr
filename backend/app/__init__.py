import time
from flask import Flask
from flask_restful import Resource, Api
from app.database import db_conn
#from config import config - Use this once we setup config.py

app = Flask(__name__)
api = Api(app)

# This config stuff could be useful https://flask.palletsprojects.com/en/2.0.x/config/
# app.config.from_object(config[config_name]) Use this once we setup config.py 

# Initialise routes                                                                            
from . import routes

# Register blueprints
from app.auth import auth_bp
app.register_blueprint(auth_bp)

# Connect to the database
db_conn()