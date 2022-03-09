from app.auth.auth import AuthResource
from app.messages.messages import send_message, Report
from . import reports_api
from . import parsers
from . import reports

class CreateReport(AuthResource):
    roles = ['mentee', 'mentor']
    @reports_api.doc(security='apiKey')
    @reports_api.expect(parsers.create_report_parser)
    def post(self):
        data = parsers.create_report_parser.parse_args()
        result = reports.create_report(self.payload['userID'], data['content'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 403

class MarkReportAsRead(AuthResource):
    roles = ['admin']
    @reports_api.doc(security='apiKey')
    @reports_api.expect(parsers.reportID_parser)
    def put(self):
        data = parsers.reportID_parser.parse_args()

        result = reports.mark_report_as_read(data['reportID'])
        if result[0]:
            return result[1], 201
        return result[1], 500



class SendReport(AuthResource):
    roles = ['mentor', 'mentee']
    @reports_api.doc(security='apiKey')
    @reports_api.expect(parsers.reportID_parser)
    def post(self):
        data = parsers.reportID_parser.parse_args()

        message = Report(-1, self.payload['userID'], data['reportID'])
        if send_message(message):
            return {'message': 'Report sent successfully.'}, 200
        return {'error': 'Failed to send report'}, 405

class GetReport(AuthResource):
    roles = ['mentor', 'mentee']
    @reports_api.doc(security='apiKey')
    def get(self):
        return reports.get_report()


    

reports_api.add_resource(CreateReport, '/create-report')
reports_api.add_resource(MarkReportAsRead, '/mark-report-as-read')
reports_api.add_resource(SendReport, '/send-report')
reports_api.add_resource(GetReport, '/get-report')