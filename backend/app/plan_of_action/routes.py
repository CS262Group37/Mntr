from app.auth.auth import AuthResource
from . import plan_api
from . import plan_of_action as plan
from . import parsers

class GetPlan(AuthResource):
    routes = ['mentor', 'mentee']
    @plan_api.expect(parsers.relationID_parser)
    @plan_api.doc(security='apiKey')
    def get(self):
        data = parsers.relationID_parser.parse_args()

        if not plan.check_relationID(self.payload['userID'], data['relationID']):
            return {'error': 'You do no have access to this plan of action'}, 401

        return plan.get_plan_of_actions(data['relationID']), 200

class MarkPlanComplete(AuthResource):
    routes = ['mentee'] # who should be able to mark a plan as correct??? Both the mentor and mentees?
    @plan_api.expect(parsers.planID_parser)
    @plan_api.doc(security='apiKey')
    def put(self):
        data = parsers.planID_parser.parse_args()
        relationID = plan.get_plan_relationID(data['planID'])
        if relationID is None:
            return {'error': 'Plan does not exist'}, 404

        if not plan.check_relationID(self.payload['userID'], relationID):
            return {'error': 'You do no have access to this plan of action'}, 401

        result = plan.mark_plan_of_action_completed(data['planID'])
        if result[0]:
            return result[1], 201
        return result[1], 500

class MarkPlanIncomplete(AuthResource):
    routes = ['mentee'] # who should be able to mark a plan as correct??? Both the mentor and mentees?
    @plan_api.expect(parsers.planID_parser)
    @plan_api.doc(security='apiKey')
    def put(self):
        data = parsers.planID_parser.parse_args()
        relationID = plan.get_plan_relationID(data['planID'])
        if relationID is None:
            return {'error': 'Plan does not exist'}, 404

        if not plan.check_relationID(self.payload['userID'], relationID):
            return {'error': 'You do no have access to this plan of action'}, 401

        result = plan.mark_plan_of_action_incompleted(data['planID'])
        if result[0]:
            return result[1], 201
        return result[1], 500

class RemovePlan(AuthResource):
    routes = ['mentee']
    @plan_api.expect(parsers.planID_parser)
    @plan_api.doc(security='apiKey')
    def delete(self):
        data = parsers.planID_parser.parse_args()
        relationID = plan.get_plan_relationID(data['planID'])
        if relationID is None:
            return {'error': 'Plan does not exist'}, 404

        if not plan.check_relationID(self.payload['userID'], relationID):
            return {'error': 'You do no have access to this plan of action'}, 401
            
        result = plan.remove_plan_of_action(data['planID'])
        if result[0]:
            return result[1], 200
        return result[1], 404

class AddPlan(AuthResource):
    routes = ['mentee']
    @plan_api.expect(parsers.plan_parser)
    @plan_api.doc(security='apiKey')
    def post(self):
        data = parsers.plan_parser.parse_args()
        if not plan.check_relationID(self.payload['userID'], data['relationID']):
            return {'error': 'You do no have access to this plan of action'}, 401

        result = plan.add_plan_of_action(data['relationID'], data['title'], data['description'])
        if result[0]:
            return result[1], 201
        return result[1], 400

plan_api.add_resource(AddPlan, '/add-plan')
plan_api.add_resource(MarkPlanComplete, '/mark-plan-complete')
plan_api.add_resource(MarkPlanIncomplete, '/mark-plan-incomplete')
plan_api.add_resource(RemovePlan, '/remove-plan')
plan_api.add_resource(GetPlan, '/get-plan')
