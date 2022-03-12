from flask_restx import reqparse

register_account_parser = reqparse.RequestParser()
register_account_parser.add_argument("email", required=True, type=str)
register_account_parser.add_argument("password", required=True, type=str)
register_account_parser.add_argument("firstName", required=True, type=str)
register_account_parser.add_argument("lastName", required=True, type=str)
register_account_parser.add_argument("profilePicture", required=False, type=str)
register_account_parser.add_argument("salt", required=True, type=str)

register_user_parser = reqparse.RequestParser()
register_user_parser.add_argument(
    "role", choices=("admin", "mentor", "mentee"), required=True, type=str
)
register_user_parser.add_argument(  # Only for mentors and mentees
    "businessArea", required=False, type=str
)
register_user_parser.add_argument(  # Only for mentors and mentees
    "topics", action="append", required=False, type=str
)
register_user_parser.add_argument(  # Only for mentees
    "skills", action="append", required=False, type=str
)
register_user_parser.add_argument(  # Only for mentees
    "ratings", action="append", required=False, type=int
)
register_user_parser.add_argument(  # Only for admins
    "adminPassword", required=False, type=str
)

login_parser = reqparse.RequestParser()
login_parser.add_argument("email", required=True)
login_parser.add_argument("password", required=True)
login_parser.add_argument("role", choices=("admin", "mentor", "mentee"), required=True)

role_parser = reqparse.RequestParser()
role_parser.add_argument("role", choices=("admin", "mentor", "mentee"), required=True)

email_parser = reqparse.RequestParser()
email_parser.add_argument("email", required=True, type=str)
