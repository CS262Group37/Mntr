from flask import Blueprint
from flask_restx import Api

auth_bp = Blueprint("auth", __name__)
auth_api = Api(auth_bp, doc="/docs/")

from . import routes
