from flask_restx import reqparse

topics_parser = reqparse.RequestParser(bundle_errors=True)
topics_parser.add_argument('topicName', required=True, type=str)

skill_parser = reqparse.RequestParser(bundle_errors=True)
skill_parser.add_argument('skillName', required = True, type=str)

user_parser = reqparse.RequestParser(bundle_errors=True)
user_parser.add_argument('userID', required = True, type = int)

business_area_parser = reqparse.RequestParser(bundle_errors=True)
business_area_parser.add_argument('businessAreaName', required = True, type = str)

feedbackID_parser = reqparse.RequestParser(bundle_errors=True)
feedbackID_parser.add_argument('feedbackID', required = True, type=int)

feedback_content_parser = reqparse.RequestParser(bundle_errors=True)
feedback_content_parser.add_argument('content', required = True, type=str)

create_report_parser = reqparse.RequestParser(bundle_errors=True)
create_report_parser.add_argument('content', required=True, type=str)

reportID_parser = reqparse.RequestParser(bundle_errors=True)
reportID_parser.add_argument('reportID', required = True, type=int)