from flask import Blueprint
from flask_restx import Api

users_bp = Blueprint("users", __name__)
users_api = Api(users_bp, doc="/docs/")

from . import routes
