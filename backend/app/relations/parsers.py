from flask_restful import reqparse

send_email_parser = reqparse.RequestParser(bundle_errors=True)
send_email_parser.add_argument('recipientID', required=True, type=int)
send_email_parser.add_argument('senderID', required=True, type=int)
send_email_parser.add_argument('contents', required=True, type=str)
