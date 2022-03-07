from flask import Blueprint                            
from flask_restx import Api
                                                       
reports_bp = Blueprint('reports', __name__) 
reports_api = Api(reports_bp, doc = '/docs/')

# Initialise the routes                                                                         
from . import routes
