from flask import Blueprint
from flask_restx import Api

relations_bp = Blueprint("relations", __name__)
relations_api = Api(relations_bp, doc="/docs/")

from . import routes
