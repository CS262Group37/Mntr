from flask import Blueprint                            
from flask_restful import Api
                                                       
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin') 
admin_api = Api(admin_bp)

# Initialise the routes                                                                         
from . import routes