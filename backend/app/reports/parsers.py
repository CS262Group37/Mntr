from flask_restx import reqparse

create_report_parser = reqparse.RequestParser(bundle_errors=True)
create_report_parser.add_argument('content', required=True, type=str)

reportID_parser = reqparse.RequestParser(bundle_errors=True)
reportID_parser.add_argument('reportID', required=True, type=int)

