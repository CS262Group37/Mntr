from app.auth.routes import AuthResource
from app.plan_of_action.plan_of_action import check_relationID
from . import meetings
from . import parsers
from . import meetings_api


class CreateMeeting(AuthResource):
    """Create a meeting on the system.
    Provided start and end time mustbe in format %d/%m/%y %H:%M

    Must be logged in as a mentee who belongs to the provided relation.
    """

    roles = ["mentee"]

    @meetings_api.expect(parsers.create_meeting_parser)
    @meetings_api.doc(security="apiKey")
    def post(self):
        data = parsers.create_meeting_parser.parse_args()

        # Check the user belongs to this relation
        if not check_relationID(self.payload["userID"], data["relationID"]):
            return {"error": "You do no have access to this relation"}, 401

        # First parse and check start and end times
        start_time = meetings.str_to_datetime(data["startTime"])
        end_time = meetings.str_to_datetime(data["endTime"])
        if (not start_time or not end_time) or (end_time > start_time):
            return {"error": "Invalid time provided"}, 400

        result = meetings.create_meeting(
            data["relationID"], start_time, end_time, data["title"], data["description"]
        )
        if result[0]:
            return result[1], 201
        else:
            return result[1], 400


class CancelMeeting(AuthResource):
    """Cancel a meeting on the system.

    Must be logged in as a mentee or menting who belongs to the provided meeting.
    """

    roles = ["mentee", "mentor"]

    @meetings_api.expect(parsers.meetingID_parser)
    @meetings_api.doc(security="apiKey")
    def put(self):
        data = parsers.meetingID_parser.parse_args()

        # Get relationID of meeting
        relationID = meetings.get_meeting_relationID(data["meetingID"])
        if relationID is None:
            return {"error": "Meeting does not exist"}, 404

        # Check the user belongs to this relation
        if not check_relationID(self.payload["userID"], relationID):
            return {"error": "You do no have access to this meeting"}, 401

        result = meetings.cancel_meeting(data["meetingID"])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 400


class AcceptMeeting(AuthResource):
    """Accept a meeting on the system.

    Must be logged in as a mentor who belongs to the provided meeting.
    """

    roles = ["mentor"]

    @meetings_api.expect(parsers.meetingID_parser)
    @meetings_api.doc(security="apiKey")
    def put(self):
        data = parsers.meetingID_parser.parse_args()

        # Get relationID of meeting
        relationID = meetings.get_meeting_relationID(data["meetingID"])
        if relationID is None:
            return {"error": "Meeting does not exist"}, 404

        # Check the user belongs to this relation
        if not check_relationID(self.payload["userID"], relationID):
            return {"error": "You do no have access to this meeting"}, 401

        result = meetings.accept_meeting(data["meetingID"])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 400


class CompleteMeeting(AuthResource):
    """Complete a meeting on the system.

    Must be logged in as a mentor who belongs to the provided meeting.
    """

    roles = ["mentor"]

    @meetings_api.expect(parsers.complete_meeting_parser)
    @meetings_api.doc(security="apiKey")
    def put(self):
        data = parsers.complete_meeting_parser.parse_args()

        # Get relationID of meeting
        relationID = meetings.get_meeting_relationID(data["meetingID"])
        if relationID is None:
            return {"error": "Meeting does not exist"}, 404

        # Check the user belongs to this relation
        if not check_relationID(self.payload["userID"], relationID):
            return {"error": "You do no have access to this meeting"}, 401

        result = meetings.complete_meeting(
            data["meetingID"], data["feedback"]
        )
        if result[0]:
            return result[1], 201
        else:
            return result[1], 400


class GetMeetings(AuthResource):
    """Get all meetings that the currently logged in user has.

    Must be logged in as a mentor or mentee that belongs to the given relation.
    """

    roles = ["mentee", "mentor"]

    @meetings_api.doc(security="apiKey")
    @meetings_api.expect(parsers.relationID_parser)
    def post(self):
        data = parsers.relationID_parser.parse_args()

        # Check the user belongs to this relation
        if not check_relationID(self.payload["userID"], data["relationID"]):
            return {"error": "You do no have access to this meeting"}, 401

        return meetings.get_meetings(data["relationID"])


class GetNextMeeting(AuthResource):
    """Get the logged in user's earliest upcoming meeting.

    Must be logged in as a mentor or mentee that belongs to the given relation.
    """

    roles = ["mentee", "mentor"]

    @meetings_api.doc(security="apiKey")
    @meetings_api.expect(parsers.relationID_parser)
    def post(self):
        data = parsers.relationID_parser.parse_args()

        # Check the user belongs to this relation
        if not check_relationID(self.payload["userID"], data["relationID"]):
            return {"error": "You do no have access to this meeting"}, 401

        return meetings.get_next_meeting(data["relationID"])


# Prefix URLs with /api/meetings/
meetings_api.add_resource(CreateMeeting, "/create-meeting")
meetings_api.add_resource(CancelMeeting, "/cancel-meeting")
meetings_api.add_resource(AcceptMeeting, "/accept-meeting")
meetings_api.add_resource(GetMeetings, "/get-meetings")
meetings_api.add_resource(GetNextMeeting, "/get-next-meeting")
meetings_api.add_resource(CompleteMeeting, "/complete-meeting")
