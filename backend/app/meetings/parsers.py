from flask_restx import reqparse

create_meeting_parser = reqparse.RequestParser()
create_meeting_parser.add_argument('relationID', required=True, type=int)
create_meeting_parser.add_argument('startTime', required=True, type=str)
create_meeting_parser.add_argument('endTime', required=True, type=str)
create_meeting_parser.add_argument('title', required=True, type=str)
create_meeting_parser.add_argument('description', required=True, type=str)

meetingID_parser = reqparse.RequestParser()
meetingID_parser.add_argument('meetingID', required=True, type=int)

complete_meeting_parser = reqparse.RequestParser()
complete_meeting_parser.add_argument('meetingID', required=True, type=int)
complete_meeting_parser.add_argument('feedback', required=True, type=str)
