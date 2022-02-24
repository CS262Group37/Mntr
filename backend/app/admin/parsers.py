from flask_restx import reqparse

topics_parser = reqparse.RequestParser(bundle_errors=True)
topics_parser.add_argument('topicName', required=True, type=str)

skill_parser = reqparse.RequestParser(bundle_errors=True)
skill_parser.add_argument('skillName', required = True, type=str)

report_parser = reqparse.RequestParser(bundle_errors=True)
report_parser.add_argument('reportID', required = True, type=int)

user_parser = reqparse.RequestParser(bundle_errors=True)
user_parser.add_argument('userID', required = True, type = int)
