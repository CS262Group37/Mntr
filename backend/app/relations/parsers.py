from flask_restful import reqparse

send_email_parser = reqparse.RequestParser(bundle_errors=True)
send_email_parser.add_argument('recipientID', required=True, type=int)
send_email_parser.add_argument('senderID', required=True, type=int)
send_email_parser.add_argument('contents', required=True, type=str)

# The mentee should send this request themselves so we can get their ID from cookie
create_relation_parser = reqparse.RequestParser(bundle_errors=True)
create_relation_parser.add_argument('mentorID', required=True, type=int)
