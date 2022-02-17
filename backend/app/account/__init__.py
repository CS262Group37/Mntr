from flask import Blueprint                            
from flask_restful import Api
                                                       
account_bp = Blueprint('account', __name__, url_prefix='/api/account') 
account_api = Api(account_bp)

# Initialise the routes                                                                         
from . import routes