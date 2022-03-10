from flask_restx import Resource

from app.auth.auth import AuthResource
from . import admin_api
from . import admin
from . import parsers
from app.messages.messages import send_message, Report

# URLs for all routes can be found at the bottom of the page.


class GetTopics(Resource):
    """Get all topics on the system.

    - No authentication required.
    """

    @admin_api.doc(security="apiKey")
    def get(self):
        return admin.get_topics(), 200


class AddTopic(AuthResource):
    """Add a topic to the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.expect(parsers.topics_parser)
    @admin_api.doc(security="apiKey")
    def post(self):
        data = parsers.topics_parser.parse_args()
        result = admin.add_topic(data["topicName"])
        if result[0]:
            return result[1], 201
        return result[1], 400


class RemoveTopic(AuthResource):
    """Remove a topic from the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.expect(parsers.topics_parser)
    @admin_api.doc(security="apiKey")
    def delete(self):
        data = parsers.topics_parser.parse_args()
        result = admin.remove_topic(data["topicName"])
        if result[0]:
            return result[1], 200
        return result[1], 404


class ClearTopics(AuthResource):
    """Clear all topics from the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.doc(security="apiKey")
    def delete(self):
        result = admin.clear_topics()
        if result[0]:
            return result[1], 200
        return result[1], 404


class GetSkills(Resource):
    """Get all skills from the system.

    No authentication required.
    """

    @admin_api.doc(security="apiKey")
    def get(self):
        return admin.get_skills(), 200


class AddSkill(AuthResource):
    """Add a skill to the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.doc(security="apiKey")
    @admin_api.expect(parsers.skill_parser)
    def post(self):
        data = parsers.skill_parser.parse_args()
        result = admin.add_skill(data["skillName"])
        if result[0]:
            return result[1], 201
        return result[1], 400


class RemoveSkill(AuthResource):
    """Remove a skill from the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.doc(security="apiKey")
    @admin_api.expect(parsers.skill_parser)
    def delete(self):
        data = parsers.skill_parser.parse_args()
        result = admin.remove_skill(data["skillName"])
        if result[0]:
            return result[1], 200
        return result[1], 404


class ClearSkills(AuthResource):
    """Clear all skills from the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.doc(security="apiKey")
    def delete(self):
        result = admin.clear_skills()
        if result[0]:
            return result[1], 200
        return result[1], 404



class GetBusinessAreas(Resource):
    """Get all business areas on the system.

    Must be logged in as an admin.
    """

    @admin_api.doc(security="apiKey")
    def get(self):
        return admin.get_business_areas(), 200


class AddBusinessArea(AuthResource):
    """Add a business area to the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.doc(security="apiKey")
    @admin_api.expect(parsers.business_area_parser)
    def post(self):
        data = parsers.business_area_parser.parse_args()
        result = admin.add_business_area(data["businessAreaName"])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 400


class ClearBusinessAreas(AuthResource):
    """Clear all business areas from the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.doc(security="apiKey")
    def delete(self):
        result = admin.clear_business_areas()
        if result[0]:
            return result[1], 200
        return result[1], 404


class RemoveBusinessArea(AuthResource):
    """Remove a business area from the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.doc(security="apiKey")
    @admin_api.expect(parsers.business_area_parser)
    def delete(self):
        data = parsers.business_area_parser.parse_args()
        result = admin.remove_business_area(data["businessAreaName"])
        if result[0]:
            return result[1], 200
        return result[1], 404


class RemoveUser(AuthResource):
    """Remove a user from the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.expect(parsers.topics_parser)
    @admin_api.doc(security="apiKey")
    def delete(self):
        data = parsers.user_parser.parse_args()
        result = admin.remove_user(data["userID"])
        if result[0]:
            return result[1], 200
        return result[1], 404

class GetAppFeedback(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def get(self):
        return admin.get_app_feedback(), 200

class CreateAppFeedback(AuthResource):
    roles = ['mentee', 'mentor']
    @admin_api.expect(parsers.feedback_content_parser)
    @admin_api.doc(security='apiKey')
    def post(self):
        data = parsers.feedback_content_parser.parse_args()
        result = admin.create_app_feedback(data['content'])
        if result[0]:
            return result[1], 201
        return result[1], 400

class MarkAppFeedbackAsRead(AuthResource):
    roles = ['admin']
    @admin_api.expect(parsers.feedbackID_parser)
    @admin_api.doc(security='apiKey')
    def put(self):
        data = parsers.feedbackID_parser.parse_args()
        result = admin.mark_app_feedback_as_read(data['feedbackID'])
        if result[0]:
            return result[1], 200
        return result[1], 404


class ClearAppFeedback(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def delete(self):
        result = admin.clear_feedback()
        if result[0]:
            return result[1], 200
        return result[1], 404


class CreateReport(AuthResource):
    roles = ['mentee', 'mentor']
    @admin_api.doc(security='apiKey')
    @admin_api.expect(parsers.create_report_parser)
    def post(self):
        data = parsers.create_report_parser.parse_args()
        result = admin.create_report(self.payload['userID'], data['content'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 403


class MarkReportAsRead(AuthResource):
    roles = ['admin']
    @admin_api.expect(parsers.reportID_parser)
    @admin_api.doc(security='apiKey')
    def put(self):
        data = parsers.reportID_parser.parse_args()
        result = admin.mark_report_as_read(data['reportID'])
        if result[0]:
            return result[1], 200
        return result[1], 404

class GetReports(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def get(self):
        return admin.get_reports(), 200

class SendReport(AuthResource):
    roles = ['mentor', 'mentee']
    @admin_api.doc(security='apiKey')
    @admin_api.expect(parsers.reportID_parser)
    def post(self):
        data = parsers.reportID_parser.parse_args()

        message = Report(-1, self.payload['userID'], data['reportID'])
        if send_message(message):
            return {'message': 'Report sent successfully.'}, 200
        return {'error': 'Failed to send report'}, 405

class ClearReports(AuthResource):
    roles = ['admin']
    @admin_api.doc(security='apiKey')
    def delete(self):
        result = admin.clear_reports()
        if result[0]:
            return result[1], 200
        return result[1], 404




admin_api.add_resource(GetTopics, '/get-topics')
admin_api.add_resource(AddTopic, '/add-topic')
admin_api.add_resource(RemoveTopic, '/remove-topic')
admin_api.add_resource(ClearTopics, '/clear-topics')
admin_api.add_resource(GetReports, '/view-reports')
admin_api.add_resource(RemoveUser, '/remove-user')
admin_api.add_resource(GetSkills, '/get-skills')
admin_api.add_resource(AddSkill, '/add-skill')
admin_api.add_resource(RemoveSkill, '/remove-skill')
admin_api.add_resource(ClearSkills, '/clear-skills')
admin_api.add_resource(AddBusinessArea, '/add-business-area')
admin_api.add_resource(RemoveBusinessArea, '/remove-business-area')
admin_api.add_resource(ClearBusinessAreas, '/clear-business-area')
admin_api.add_resource(GetBusinessAreas, '/get-business-area')
admin_api.add_resource(GetAppFeedback, '/get-app-feedback')
admin_api.add_resource(CreateAppFeedback, '/create-app-feedback')
admin_api.add_resource(MarkAppFeedbackAsRead, '/mark-app-feeback-as-read')
admin_api.add_resource(ClearAppFeedback, '/clear-app-feedback')
admin_api.add_resource(MarkReportAsRead, '/mark-report-as-read')
admin_api.add_resource(GetReports, '/view-reports')
admin_api.add_resource(CreateReport, '/create-report')
admin_api.add_resource(SendReport, '/send-report')
admin_api.add_resource(ClearReports, '/clear-reports')

