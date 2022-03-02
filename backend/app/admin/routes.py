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
        result = admin.add_topic(data['topicName'])
        if result[0]:
            return result[1]
        return result[1]

class RemoveTopic(AuthResource):
    roles = ['admin']
    @admin_api.expect(parsers.topics_parser)
    @admin_api.doc(security='apiKey')
    def post(self):
        data = parsers.topics_parser.parse_args()
        result = admin.remove_topic(data['topicName'])
        if result[0]:
            return result[1]
        return result[1]

class ClearTopics(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def delete(self):
        result = admin.clear_topics()
        if result[0]:
            return result[1]
        return result[1]

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
        result = admin.remove_user(data['userID'])
        if result[0]:
            return result[1]
        return result[1]

class MarkReportAsRead(AuthResource):
    roles = ['admin']
    @admin_api.expect(parsers.report_parser)
    @admin_api.doc(security='apiKey')
    def post(self):
        data = parsers.report_parser.parse_args()
        result = admin.mark_report_as_read(data['reportID'])
        if result[0]:
            return result[1]
        return result[1]

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
        result = admin.add_skill(data['skillName'])
        if result[0]:
            return result[1]
        return result[1]

class RemoveSkill(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    @admin_api.expect(parsers.skill_parser)
    def post(self):
        data = parsers.skill_parser.parse_args()
        result = admin.remove_skill(data['skillName'])
        if result[0]:
            return result[1]
        return result[1]

class ClearSkills(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def delete(self):
        result = admin.clear_skills()
        if result[0]:
            return result[1]
        return result[1]

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
