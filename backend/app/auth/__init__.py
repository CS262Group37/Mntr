from flask import Blueprint                            
from flask_restful import Api
                                                       
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth') 
auth_api = Api(auth_bp)

# Initialise the routes                                                                            
from app.auth import routes
