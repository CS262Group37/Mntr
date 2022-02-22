from flask_restx import reqparse

register_account_parser = reqparse.RequestParser(bundle_errors=True)
register_account_parser.add_argument('email', required=True, type=str)
register_account_parser.add_argument('password', required=True, type=str)
register_account_parser.add_argument('firstName', required=True, type=str)
register_account_parser.add_argument('lastName', required=True, type=str)

register_user_parser = reqparse.RequestParser(bundle_errors=True)
register_user_parser.add_argument('role', choices=('admin', 'mentor', 'mentee'), required=True, type=str)

login_parser = reqparse.RequestParser(bundle_errors=True)
login_parser.add_argument('email', required=True)
login_parser.add_argument('password', required=True)
login_parser.add_argument('role', choices=('admin', 'mentor', 'mentee'), required=True)
