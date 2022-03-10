from flask_restx import Resource

from app.auth.auth import AuthResource
from . import admin_api
from . import admin
from . import parsers

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


class GetReports(AuthResource):
    """Get all reports from the system.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.doc(security="apiKey")
    def get(self):
        return admin.get_reports(), 200


class MarkReportAsRead(AuthResource):
    """Mark a report as read.

    Must be logged in as an admin.
    """

    roles = ["admin"]

    @admin_api.expect(parsers.report_parser)
    @admin_api.doc(security="apiKey")
    def put(self):
        data = parsers.report_parser.parse_args()
        result = admin.mark_report_as_read(data["reportID"])
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


# Prefix URLs with /api/admin/
admin_api.add_resource(GetTopics, "/get-topics")
admin_api.add_resource(AddTopic, "/add-topic")
admin_api.add_resource(RemoveTopic, "/remove-topic")
admin_api.add_resource(ClearTopics, "/clear-topics")
admin_api.add_resource(GetReports, "/view-reports")
admin_api.add_resource(RemoveUser, "/remove-user")
admin_api.add_resource(MarkReportAsRead, "/mark-report-as-read")
admin_api.add_resource(GetSkills, "/get-skills")
admin_api.add_resource(AddSkill, "/add-skill")
admin_api.add_resource(RemoveSkill, "/remove-skill")
admin_api.add_resource(ClearSkills, "/clear-skills")
admin_api.add_resource(AddBusinessArea, "/add-business-area")
admin_api.add_resource(RemoveBusinessArea, "/remove-business-area")
admin_api.add_resource(ClearBusinessAreas, "/clear-business-area")
admin_api.add_resource(GetBusinessAreas, "/get-business-area")
