from flask_restful import reqparse

# Put global parsers in here
userID_parser = reqparse.RequestParser()
userID_parser.add_argument('userID', required=True, type=int)
