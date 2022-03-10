from flask import Blueprint
from flask_restx import Api

admin_bp = Blueprint("admin", __name__)
admin_api = Api(admin_bp, doc="/docs/")

from . import routes
