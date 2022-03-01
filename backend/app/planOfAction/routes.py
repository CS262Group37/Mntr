from app.auth.routes import AuthResource
from . import plan_api
from . import planOfAction as plan
from . import parsers

class CreatePlan(AuthResource):
    @plan_api.expect(parsers.plan_parser)
    def post(self):
        data = parsers.plan_parser.parse_args()
        result = plan.create_plan_of_action(data['relationID'], data['title'], data['description'])
        if result[0]:
            return result[1]
        return result[1]

class GetPlan(AuthResource):
    @plan_api.expect(parsers.relationID_parser)
    def get(self):
        data = parsers.relationID_parser.parse_args()
        return plan.get_plan_of_actions(data['relationID'])

class GetAllPlans(AuthResource):
    def get(self):
        return plan.get_all_plan_of_actions()

class MarkPlanComplete(AuthResource):
    def post(self):
        data = parsers.planID_parser.parse_args()
        result = plan.mark_plan_of_action_completed(data['planID'])
        if result[0]:
            return result[1]
        return result[1]

class RemovePlan(AuthResource):
    @plan_api.expect(parsers.planID_parser)
    def post(self):
        data = parsers.planID_parser.parse_args()
        result = plan.remove_topic(data['planID'])
        if result[0]:
            return result[1]
        return result[1]

class AddMilestone(AuthResource):
    @plan_api.expect(parsers.milestone_parser)
    def post(self):
        data = parsers.milestone_parser.parse_args()
        result = plan.add_milestone(data['planID'], data['title'], data['description'])
        if result[0]:
            return result[1]
        return result[1]

class MarkMilestoneComplete(AuthResource):
    def post(self):
        data = parsers.milestoneID_parser.parse_args()
        result = plan.mark_milestone_of_action_completed(data['milestoneID'])
        if result[0]:
            return result[1]
        return result[1]

class RemoveMilestone(AuthResource):
    @plan_api.expect(parsers.milestoneID_parser)
    def post(self):
        data = parsers.milestoneID_parser.parse_args()
        result = plan.remove_topic(data['milestoneID'])
        if result[0]:
            return result[1]
        return result[1]

class ViewMilestone(AuthResource):
    @plan_api.expect(parsers.milestoneID_parser)
    def post(self):
        data = parsers.milestoneID_parser.parse_args()
        result = plan.mark_milestone_as_completed(data['milestoneID'])
        if result[0]:
            return result[1]
        return result[1]

plan_api.add_resource(CreatePlan, '/create-plan')
plan_api.add_resource(AddMilestone, '/add-milestone')
plan_api.add_resource(MarkPlanComplete, '/set-plan-complete')
plan_api.add_resource(RemovePlan, '/remove-plan')
plan_api.add_resource(GetPlan, '/get-plan')
plan_api.add_resource(GetAllPlans, '/get-all-plans')
plan_api.add_resource(MarkMilestoneComplete, '/set-milestone-complete')
plan_api.add_resource(RemoveMilestone, '/remove-milestone')
plan_api.add_resource(ViewMilestone, '/view-milestone')
