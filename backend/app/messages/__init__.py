from flask import Blueprint                            
from flask_restx import Api
                                                       
messages_bp = Blueprint('messages', __name__) 
messages_api = Api(messages_bp)

# Initialise the routes                                                                         
from . import routes