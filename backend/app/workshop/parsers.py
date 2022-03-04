from flask_restx import reqparse

workshop_parser = reqparse.RequestParser(bundle_errors=True)
workshop_parser.add_argument('mentorID',required=True, type=str)
workshop_parser.add_argument('title',required=True, type=str)
workshop_parser.add_argument('topic',required=True, type=str)
workshop_parser.add_argument('description',required=True, type=str)
workshop_parser.add_argument('time',required=True, type=str)
workshop_parser.add_argument('duration',required=True, type=str)
workshop_parser.add_argument('location',required=True, type=str)

workshopID_parser = reqparse.RequestParser()
workshopID_parser.add_argument('workshopID', required=True, type=int)