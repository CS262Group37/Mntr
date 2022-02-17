from flask import Blueprint                            
from flask_restful import Api
                                                       
meetings_bp = Blueprint('meetings', __name__, url_prefix='/api/meetings') 
meetings_api = Api(meetings_bp)

# Initialise the routes                                                                         
from . import routes