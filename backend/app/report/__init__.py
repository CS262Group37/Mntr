from flask import Blueprint                            
from flask_restx import Api
                                                       
report_bp = Blueprint('report', __name__) 
report_api = Api(report_bp, doc = '/docs/')

# Initialise the routes                                                                         
from . import routes
