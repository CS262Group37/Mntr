from . import plan_api
from . import planOfAction
from . import parsers

def CreatePlan():
    @plan_api.expect(parsers.plan_parser)
    def post(self):
        data = parser.plan_parser.parse_args()
        result = plan.create_plan_of_action(data['relationID'], data['title'], data['description'])
        if result[0]:
            return result[1]
        return result[1]

def GetPlan():
    def get(self):
        return plan.get_plan_of_actions()

def MarkPlanComplete():
    def post(self):
        data = parsers.planID_parser.parse_args()
        result = plan.mark_plan_of_action_completed(data['planID'])
        if result[0]:
            return result[1]
        return result[1]

def RemovePlan():
    @plan_api.expect(parsers.planID_parser)
    def post(self):
        data = parsers.planID_parser.parse_args()
        result = admin.remove_topic(data['planID'])
        if result[0]:
            return result[1]
        return result[1]

def AddMilestone():
    @plan_api.expect(parsers.milestone_parser)
    def post(self):
        data = parser.milestone_parser.parse_args()
        result = plan.add_milestone(data['planID'], data['title'], data['description'])
        if result[0]:
            return result[1]
        return result[1]

def MarkMilestoneComplete():
    def post(self):
        data = parsers.milestoneID_parser.parse_args()
        result = plan.mark_milestone_of_action_completed(data['milestoneID'])
        if result[0]:
            return result[1]
        return result[1]










admin_api.add_resource(CreatePlan, '/create-plan')
admin_api.add_resource(AddMilestone, '/add-milestone')
