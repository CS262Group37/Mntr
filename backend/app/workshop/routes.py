from app.auth.routes import AuthResource
from app.messages.messages import send_message
from . import workshop_api
from . import parsers
from . import workshop

class CreateWorkshop(AuthResource):
    @workshop_api.doc(security='apiKey')
    @workshop_api.expect(parsers.workshop_parser)
    def post(self):
        data = parsers.workshop_parser.parse_args()
        result = workshop.schedule_workshop(data['mentorID'], data['title'], data['topic'], data['desc'], data['time'], data['duration'], data['location'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 500
        
workshop_api.add_resource(CreateWorkshop, '/create-workshop')
