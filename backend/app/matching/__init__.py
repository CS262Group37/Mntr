from flask import Blueprint                            
from flask_restful import Api
                                                       
matching_bp = Blueprint('matching', __name__, url_prefix='/api/matching') 
matching_api = Api(matching_bp)

# Initialise the routes                                                                         
from . import routes