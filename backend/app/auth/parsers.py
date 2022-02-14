from flask_restful import reqparse

# Store parsers for auth requests in here
# Apparently this reqparse class is depreciated by it seems easier to use than marshmallow so I might just use it anyway

register_parser = reqparse.RequestParser(bundle_errors=True)
register_parser.add_argument('email', required=True, type=str)
register_parser.add_argument('password', required=True, type=str)
register_parser.add_argument('firstName', required=True, type=str)
register_parser.add_argument('lastName', required=True, type=str)
register_parser.add_argument('role', required=True, type=str)

login_parser = reqparse.RequestParser(bundle_errors=True)
login_parser.add_argument('email', required=True)
login_parser.add_argument('password', required=True)
