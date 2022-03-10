from flask_restx import reqparse

get_users_parser = reqparse.RequestParser(bundle_errors=True)
get_users_parser.add_argument("userID", required=True, type=int)
