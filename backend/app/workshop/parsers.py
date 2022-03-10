from flask_restx import reqparse

create_workshop_parser = reqparse.RequestParser(bundle_errors=True)
create_workshop_parser.add_argument('mentorID',required=True, type=int)
create_workshop_parser.add_argument('title',required=True, type=str)
create_workshop_parser.add_argument('topic',required=True, type=str)
create_workshop_parser.add_argument('desc',required=True, type=str)
create_workshop_parser.add_argument('startTime',required=True, type=str)
create_workshop_parser.add_argument('endTime',required=True, type=str)
create_workshop_parser.add_argument('location',required=True, type=str)

cancel_workshop_parser = reqparse.RequestParser()
cancel_workshop_parser.add_argument('workshopID', required=True, type=int)

get_workshops_parser = reqparse.RequestParser()
get_workshops_parser.add_argument('userID',required=True,type=int)
get_workshops_parser.add_argument('role',required=True,type=str)

view_workshop_attendee_parser = reqparse.RequestParser()
view_workshop_attendee_parser.add_argument('workshopID', required=True, type=int)