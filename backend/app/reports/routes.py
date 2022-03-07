from app.auth.routes import AuthResource
from app.messages.messages import send_message, Email
from . import report_api
from . import parsers
from . import report

class CreateReport(AuthResource):
    roles = ['mentee', 'mentor']
    @relations_api.doc(security='apiKey')
    @relations_api.expect(parsers.create_report_parser)
    def post(self):
        data = parsers.create_report_parser.parse_args()
        result = reports.create_report(self.payload['userID'], data['content'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 403

reports_api.add_resource(CreateReport, '/create-report')