from flask import Blueprint
from flask_restx import Api

plan_bp = Blueprint("plan", __name__)
plan_api = Api(plan_bp, doc="/docs/")

# Initialise the routes
from . import routes
