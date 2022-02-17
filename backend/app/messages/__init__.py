from flask import Blueprint                            
from flask_restful import Api
                                                       
messages_bp = Blueprint('messages', __name__, url_prefix='/api/messages') 
messages_api = Api(messages_bp)

# Initialise the routes                                                                         
from . import routes