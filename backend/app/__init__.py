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
    database.load_schema()

# Register blueprints
from app.auth import auth_bp
app.register_blueprint(auth_bp)

from app.matching import matching_bp
app.register_blueprint(matching_bp)

from app.meetings import meetings_bp
app.register_blueprint(meetings_bp)

from app.messages import messages_bp
app.register_blueprint(messages_bp)

from app.relations import relations_bp
app.register_blueprint(relations_bp)