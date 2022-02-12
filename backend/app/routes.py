from flask_restful import Resource
from . import api
import time
from app.database import db_close

# Resource routing using flask-RESTful https://flask-restful.readthedocs.io/en/latest/quickstart.html

# All of the routes defined in this file will have no prefix. Should be used for general API calls. 

# These are temporary for testing
class Time(Resource):
    def get(self):
        return {'time': time.time()}

class HelloWorld(Resource):
    def get(self):
        return "<p>Hello, World!</p>"

class CloseDatabase(Resource):
    def get(self):
        db_close()
        return "<H1>Database closed!</H1>"

api.add_resource(Time, '/time')
api.add_resource(HelloWorld, '/')
api.add_resource(CloseDatabase, '/close')