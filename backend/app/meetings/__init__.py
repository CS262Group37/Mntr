from flask import Blueprint                            
from flask_restx import Api
                                                       
meetings_bp = Blueprint('meetings', __name__) 
meetings_api = Api(meetings_bp)

# Initialise the routes                                                                         
from . import routes