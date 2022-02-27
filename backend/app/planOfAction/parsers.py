from flask_restx import reqparse

plan_parser = reqparse.RequestParser(bundle_errors=True)
plan_parser.add_argument('relationID', required=True, type=int)
plan_parser.add_argument('title', required=True, type=str)
plan_parser.add_argument('description', required=True, type=str)

planID_parser = reqparse.RequestParser(bundle_errors=True)
planID_parser.add_argument('planID', required=True, type=int)

milestone_parser = reqparse.RequestParser(bundle_errors=True)
milestone_parser.add_argument('relationID', required=True, type=int)
milestone_parser.add_argument('title', required=True, type=str)
milestone_parser.add_argument('description', required=True, type=str)


