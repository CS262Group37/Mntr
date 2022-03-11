from flask import Blueprint
from flask_restx import Api

workshop_bp = Blueprint("workshop", __name__)
workshop_api = Api(workshop_bp, doc="/docs/")

from . import routes
