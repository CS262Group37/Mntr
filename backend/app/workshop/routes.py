from app.meetings.meetings import str_to_datetime
from app.auth.auth import AuthResource
from . import workshop_api
from . import parsers
from . import workshop


class CreateWorkshop(AuthResource):
    roles = ["mentor"]

    @workshop_api.doc(security="apiKey")
    @workshop_api.expect(parsers.create_workshop_parser)
    def post(self):
        data = parsers.create_workshop_parser.parse_args()

        # First parse and check start and end times
        start_time = str_to_datetime(data["startTime"])
        end_time = str_to_datetime(data["endTime"])
        if (not start_time or not end_time) or (end_time < start_time):
            return {"error": "Invalid time provided"}, 400

        result = workshop.create_workshop(
            data["mentorID"],
            data["title"],
            data["topic"],
            data["desc"],
            start_time,
            end_time,
            data["location"],
        )
        if result[0]:
            return result[1], 201
        else:
            return result[1], 500


class CancelWorkshop(AuthResource):
    roles = ["mentor"]

    @workshop_api.doc(security="apiKey")
    @workshop_api.expect(parsers.cancel_workshop_parser)
    def post(self):
        data = parsers.cancel_workshop_parser.parse_args()
        result = workshop.cancel_workshop(data["workshopID"])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 500


class GetWorkshops(AuthResource):
    roles = ["mentor", "mentee"]

    @workshop_api.doc(security="apiKey")
    @workshop_api.expect(parsers.get_workshops_parser)
    def get(self):
        data = parsers.get_workshops_parser.parse_args()
        return workshop.get_workshops(data["userID"], data["role"]), 201


class ViewWorkshopAttendee(AuthResource):
    roles = ["mentor", "mentee"]

    @workshop_api.doc(security="apiKey")
    @workshop_api.expect(parsers.view_workshop_attendee_parser)
    def get(self):
        data = parsers.view_workshop_attendee_parser.parse_args()
        return workshop.view_workshop_attendee(data["workshopID"])


class JoinWorkshop(AuthResource):
    roles = ["mentee"]

    @workshop_api.doc(security="apiKey")
    @workshop_api.expect(parsers.join_workshop_parser)
    def post(self):
        data = parsers.join_workshop_parser.parse_args()
        result = workshop.join_workshop(self.payload["userID"], data["workshopID"])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 500


workshop_api.add_resource(CreateWorkshop, "/create-workshop")
workshop_api.add_resource(CancelWorkshop, "/cancel-workshop")
workshop_api.add_resource(GetWorkshops, "/get-workshops")
workshop_api.add_resource(ViewWorkshopAttendee, "view-workshop-attendee")
workshop_api.add_resource(JoinWorkshop, "/join-workshop")
