from flask_restx import reqparse

get_messages_parser = reqparse.RequestParser(bundle_errors=True)
get_messages_parser.add_argument('userID', required=True, type=int)
