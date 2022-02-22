from flask import Flask, url_for, make_response
from flask_restx import Api, apidoc

import config
import app.auth as auth
import app.matching as matching
import app.meetings as meetings
import app.messages as messages
import app.relations as relations
from . import database as db

# Good description of the pattern I'm trying to implement: http://exploreflask.com/en/latest/blueprints.html

def create_app():
    """Initialise the application."""
    app = Flask(__name__)
    api = Api(app, authorizations=config.authorizations, doc='/docs/')
    app.config.from_object(config.DevConfig)

    # Initialise database
    with app.app_context():
        db.init_db()
        db.load_schema()
    
        # Register blueprints
        app.register_blueprint(auth.auth_bp, url_prefix='/api/auth')
        app.register_blueprint(matching.matching_bp, url_prefix='/api/matching')
        app.register_blueprint(meetings.meetings_bp, url_prefix='/api/meetings')
        app.register_blueprint(messages.messages_bp, url_prefix='/api/messages')
        app.register_blueprint(relations.relations_bp, url_prefix='/api/relations')

    return app
