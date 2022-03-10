from app.auth.auth import AuthResource
from app.messages.messages import send_message
from . import workshop_api
from . import parsers
from . import workshop

class CreateWorkshop(AuthResource):
    @workshop_api.doc(security='apiKey')
    @workshop_api.expect(parsers.create_workshop_parser)
    def post(self):
        data = parsers.create_workshop_parser.parse_args()
        result = workshop.create_workshop(data['mentorID'], data['title'], data['topic'], data['desc'], data['startTime'], data['endTime'], data['location'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 500
class CancelWorkshop(AuthResource):
    @workshop_api.doc(security='apiKey')
    @workshop_api.expect(parsers.cancel_workshop_parser)
    def post(self):
        data = parsers.cancel_workshop_parser.parse_args()
        result = workshop.cancel_workshop(data['workshopID'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 500
class GetWorkshops(AuthResource):
    @workshop_api.doc(security='apiKey')
    @workshop_api.expect(parsers.get_workshops_parser)
    def get(self):
        data = parsers.get_workshops_parser.parse_args()
        return workshop.get_workshops(data['userID'], data['role']), 201

class ViewWorkshopAttendee(AuthResource):
    @workshop_api.doc(security='apiKey')
    @workshop_api.expect(parsers.view_workshop_attendee_parser)
    def get(self):
        data = parsers.view_workshop_attendee_parser.parse_args()
        result = workshop.view_workshop_attendee(data['workshopID'])
        if result:
            return result, 201
        else:
            return result, 500
workshop_api.add_resource(CreateWorkshop, '/create-workshop')
workshop_api.add_resource(CancelWorkshop,'/cancel-workshop')
workshop_api.add_resource(GetWorkshops,'/get-workshops')
workshop_api.add_resource(ViewWorkshopAttendee,'view-workshop-attendee')
