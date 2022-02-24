from app.auth.routes import AuthResource
from . import admin_api
from . import admin
from . import parsers

class GetTopics(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def get(self):
        return admin.get_topics()

class AddTopic(AuthResource):
    roles = ['admin']
    @admin_api.expect(parsers.topics_parser)
    @admin_api.doc(security='apiKey')
    def post(self):
        data = parsers.topics_parser.parse_args()
        return admin.add_topic(data['topicName'])

class RemoveTopic(AuthResource):
    roles = ['admin']
    @admin_api.expect(parsers.topics_parser)
    @admin_api.doc(security='apiKey')
    def post(self):
        data = parsers.topics_parser.parse_args()
        return admin.remove_topic(data['topicName'])

class ClearTopics(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def delete(self):
        return admin.clear_topics()

class ViewReports(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def get(self):
        return admin.get_reports()

class RemoveUser(AuthResource):
    roles = ['admin']
    @admin_api.expect(parsers.topics_parser)
    @admin_api.doc(security='apiKey')
    def post(self):
        data = parsers.user_parser.parse_args()
        return admin.remove_user(data['userID'])

class MarkReportAsRead(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def post(self):
        data = parsers.report_parser.parse_args()
        return admin.mark_report_as_read(data['reportID'])

class GetSkills(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def get(self):
        return admin.get_skills()

class AddSkill(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    @admin_api.expect(parsers.skill_parser)
    def post(self):
        data = parsers.skill_parser.parse_args()
        return admin.add_skill(data['skillName'])

class RemoveSkill(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    @admin_api.expect(parsers.skill_parser)
    def post(self):
        data = parsers.skill_parser.parse_args()
        return admin.remove_skill(data['skillName'])

class ClearSkills(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def delete(self):
        return admin.clear_skills()

class AddBusinessArea(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    @admin_api.expect(parsers.business_area_parser)
    def post(self):
        data = parsers.business_area_parser.parse_args()
        return admin.add_business_area(data['businessAreaName'])

class RemoveBusinessArea(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    @admin_api.expect(parsers.business_area_parser)
    def post(self):
        data = parsers.business_area_parser.parse_args()
        return admin.remove_business_area(data['businessAreaName'])

class ClearBusinessAreas(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def delete(self):
        return admin.clear_business_areas()

admin_api.add_resource(GetTopics, '/get-topics')
admin_api.add_resource(AddTopic, '/add-topic')
admin_api.add_resource(RemoveTopic, '/remove-topic')
admin_api.add_resource(ClearTopics, '/clear-topics')
admin_api.add_resource(ViewReports, '/view-reports')
admin_api.add_resource(RemoveUser, '/remove-user')
admin_api.add_resource(MarkReportAsRead, '/mark-report-as-read')
admin_api.add_resource(GetSkills, '/get-skills')
admin_api.add_resource(AddSkill, '/add-skill')
admin_api.add_resource(RemoveSkill, '/remove-skill')
admin_api.add_resource(ClearSkills, '/clear-skills')
admin_api.add_resource(AddBusinessArea, '/add-business-area')
admin_api.add_resource(RemoveBusinessArea, '/remove-business-area')
admin_api.add_resource(ClearBusinessAreas, '/clear-business-area')
