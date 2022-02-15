from flask_restful import Resource
from app import api
import time

# Resource routing using flask-RESTful https://flask-restful.readthedocs.io/en/latest/quickstart.html

# All of the routes defined in this file will have no prefix. Should be used for general API calls. 

# These are temporary for testing
class Time(Resource):
    def get(self):
        return {'time': time.time()}

class HelloWorld(Resource):
    def get(self):
        return "<p>Hello, World!</p>"

api.add_resource(Time, '/api/time')
api.add_resource(HelloWorld, '/api/')
