from flask_restx import reqparse

create_report_parser = reqparse.RequestParser(bundle_errors=True)
create_report_parser.add_argument('content', required=True, type=str)