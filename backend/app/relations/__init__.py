from flask import Blueprint                            
from flask_restful import Api
                                                       
relations_bp = Blueprint('relations', __name__, url_prefix='/api/relations') 
relations_api = Api(relations_bp)

# Initialise the routes                                                                         
from . import routes