from flask import Blueprint                            
from flask_restx import Api
                                                       
matching_bp = Blueprint('matching', __name__) 
matching_api = Api(matching_bp)

# Initialise the routes                                                                         
from . import routes