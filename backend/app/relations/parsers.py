from flask_restx import reqparse

send_email_parser = reqparse.RequestParser(bundle_errors=True)
send_email_parser.add_argument("recipientID", required=True, type=int)
send_email_parser.add_argument("subject", required=True, type=str)
send_email_parser.add_argument("content", required=True, type=str)

create_relation_parser = reqparse.RequestParser(bundle_errors=True)
create_relation_parser.add_argument("mentorID", required=True, type=int)
