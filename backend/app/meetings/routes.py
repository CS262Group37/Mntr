from app.auth.routes import AuthResource
from app.plan_of_action.plan_of_action import check_relationID
from . import meetings
from . import parsers
from . import meetings_api

# Start and end time format must be '09/19/18 13:55:26'
class CreateMeeting(AuthResource):
    roles = ['mentee']

    @meetings_api.expect(parsers.create_meeting_parser)
    @meetings_api.doc(security='apiKey')
    def post(self):
        data = parsers.create_meeting_parser.parse_args()
        if not check_relationID(self.payload['userID'], data['relationID']):
            return {'error': 'You do no have access to this relation'}, 401

        # First parse start and end time
        start_time = meetings.str_to_datetime(data['startTime'])
        end_time = meetings.str_to_datetime(data['endTime'])
        if (not start_time or not end_time) and (end_time > start_time):
            return {'error': 'Invalid time provided'}, 400
        
        result = meetings.create_meeting(data['relationID'], start_time, end_time, data['title'], data['description'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 400

class CancelMeeting(AuthResource):
    roles = ['mentee', 'mentor']
    
    @meetings_api.expect(parsers.meetingID_parser)
    @meetings_api.doc(security='apiKey')
    def put(self):
        data = parsers.meetingID_parser.parse_args()
        # Now get relationID of meeting
        relationID = meetings.get_meeting_relationID(data['meetingID'])
        if relationID is None:
            return {'error': 'Meeting does not exist'}, 404
        
        # Check this is the callers meeting
        if not check_relationID(self.payload['userID'], relationID):
            return {'error': 'You do no have access to this relation'}, 401

        result = meetings.cancel_meeting(data['meetingID'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 400

class AcceptMeeting(AuthResource):
    roles = ['mentor']
    
    @meetings_api.expect(parsers.meetingID_parser)
    @meetings_api.doc(security='apiKey')
    def put(self):
        data = parsers.meetingID_parser.parse_args()
        # Now get relationID of meeting
        relationID = meetings.get_meeting_relationID(data['meetingID'])
        if relationID is None:
            return {'error': 'Meeting does not exist'}, 404
        
        # Check this is the callers meeting
        if not check_relationID(self.payload['userID'], relationID):
            return {'error': 'You do no have access to this relation'}, 401

        result = meetings.accept_meeting(data['meetingID'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 400

class CompleteMeeting(AuthResource):
    roles = ['mentor']
    
    @meetings_api.expect(parsers.complete_meeting_parser)
    @meetings_api.doc(security='apiKey')
    def put(self):
        data = parsers.complete_meeting_parser.parse_args()
        # Now get relationID of meeting
        relationID = meetings.get_meeting_relationID(data['meetingID'])
        if relationID is None:
            return {'error': 'Meeting does not exist'}, 404
        
        # Check this is the callers meeting
        if not check_relationID(self.payload['userID'], relationID):
            return {'error': 'You do no have access to this relation'}, 401

        result = meetings.complete_meeting(self.payload['userID'], data['meetingID'], data['feedback'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 400

class GetMeetings(AuthResource):
    roles = ['mentee', 'mentor']

    @meetings_api.doc(security='apiKey')
    def get(self):
        return meetings.get_meetings(self.payload['userID'], self.payload['role'])

meetings_api.add_resource(CreateMeeting, '/create-meeting')
meetings_api.add_resource(CancelMeeting, '/cancel-meeting')
meetings_api.add_resource(AcceptMeeting, '/accept-meeting')
meetings_api.add_resource(GetMeetings, '/get-meetings')
meetings_api.add_resource(CompleteMeeting, '/complete-meeting')
