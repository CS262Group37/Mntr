import time
from flask import Flask
from flask_restful import Resource, Api
from app.database import db_conn
import config

app = Flask(__name__)
api = Api(app)

# Apply desired config from config.py
app.config.from_object(config.DevConfig)

# Initialise routes                                                                            
from . import routes

# Register blueprints
from app.auth import auth_bp
app.register_blueprint(auth_bp)

# Connect to the database
db_conn()