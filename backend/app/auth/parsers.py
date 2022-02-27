from flask_restx import reqparse

register_account_parser = reqparse.RequestParser()
register_account_parser.add_argument('email', required=True, type=str)
register_account_parser.add_argument('password', required=True, type=str)
register_account_parser.add_argument('firstName', required=True, type=str)
register_account_parser.add_argument('lastName', required=True, type=str)

register_user_parser = reqparse.RequestParser()
register_user_parser.add_argument('role', choices=('admin', 'mentor', 'mentee'), required=True, type=str)
# Only for mentors and mentees
register_user_parser.add_argument('businessArea', required=False, type=str)
register_user_parser.add_argument('topics', action='append', required=False, type=str)
# Only for mentees
register_user_parser.add_argument('skills', action='append', required=False, type=str)
register_user_parser.add_argument('ratings', action='append', required=False, type=int)
# Only for admins
register_user_parser.add_argument('adminPassword', required=False, type=str)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', required=True)
login_parser.add_argument('password', required=True)
login_parser.add_argument('role', choices=('admin', 'mentor', 'mentee'), required=True)
