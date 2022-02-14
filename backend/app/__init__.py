from flask import Flask
from flask_restful import Api
import config

# TODO: Eventually switch this to a factory design pattern but this is fine for now

# Create app
app = Flask(__name__)
api = Api(app)

# Apply desired config from config.py
app.config.from_object(config.DevConfig)

# Initialise routes                                                                            
from app import routes

# Connect to the database
from . import database
with app.app_context():
    database.create_connection_pool()
    database.build()

# Register blueprints
from app.auth import auth_bp
app.register_blueprint(auth_bp)
