from flask import Flask
from flask_restful import Api
import config

# Create app
app = Flask(__name__)
api = Api(app)

# Apply desired config from config.py
app.config.from_object(config.DevConfig)

# Initialise routes                                                                            
from app import routes

# Connect to the database
from . import database
database.connect()
database.build()

# Register blueprints
from app.auth import auth_bp
app.register_blueprint(auth_bp)
