from flask import make_response
from flask_restx import Resource

from . import auth_api
from . import auth
from . import parsers


class RegisterAccount(Resource):
    """Register an account on the system.

    No authentication required.
    """

    @auth_api.expect(parsers.register_account_parser)
    def post(self):
        data = parsers.register_account_parser.parse_args()
        result = auth.register_account(
            data["email"],
            data["password"],
            data["firstName"],
            data["lastName"],
            data["profilePicture"],
        )

        if result[0]:
            # Generate a JWT token for the account
            token = auth.encode_token(data["email"])
            if not token[0]:
                return token[1], 403

            # Set the token cookie in response
            response = make_response(result[1], 201)
            response.set_cookie("JWT_Token", token[1], httponly=True, samesite="Lax")
            return response
        else:
            return result[1], 403


class RegisterUser(auth.AuthResource):
    """Register a user on the system.

    Must be authenticated as a logged in account.
    """

    @auth_api.expect(parsers.register_user_parser)
    def post(self):
        data = parsers.register_user_parser.parse_args()
        result = auth.register_user(self.payload["accountID"], data)
        if result[0]:
            # Login as the registered user
            token = auth.encode_token(self.payload["email"], self.payload["role"])
            if not token[0]:
                return token[1], 403

            # Set the token cookie in response
            response = make_response(result[1], 201)
            response.set_cookie("JWT_Token", token[1], httponly=True, samesite="Lax")
            return response
        else:
            return result[1], 403


class Login(Resource):
    """Login as a registered user on the system.

    Must provide the role to login as.
    No authentication required.
    """

    @auth_api.expect(parsers.login_parser)
    def post(self):
        data = parsers.login_parser.parse_args()
        print(f"Trying to login as {data['email']} with password {data['password']}.")
        if not auth.check_email(data["email"]):
            return {"error": "Invalid email or password"}, 401

        if not auth.check_password(data["email"], data["password"]):
            return {"error": "Invalid email or password"}, 401

        token_result = auth.encode_token(data["email"], data["role"])
        if not token_result[0]:
            return token_result[1], 403

        response = make_response({"message": "Successfully logged in"}, 200)
        response.set_cookie("JWT_Token", token_result[1], httponly=True, samesite="Lax")

        return response


class Logout(Resource):
    """Logout user by clearing cookie value.

    No authentication required.
    """

    def get(self):
        response = make_response({"message": "Successfully logged out"}, 200)
        response.set_cookie("JWT_Token", "", expires="Thu, 01 Jan 1970 00:00:00 GMT")
        return response


class ChangeRole(auth.AuthResource):
    """Change the role of a logged in account.

    Must be logged with a valid account.
    """

    @auth_api.expect(parsers.role_parser)
    def post(self):
        data = parsers.role_parser.parse_args()

        token_result = auth.encode_token(self.payload["email"], data["role"])
        if not token_result[0]:
            return token_result[1]

        response = make_response({"message": "Successfully changed role"}, 200)
        response.set_cookie("JWT_Token", token_result[1], httponly=True, samesite="Lax")

        return response


# Prefix URLs with /api/auth/
auth_api.add_resource(RegisterAccount, "/register-account")
auth_api.add_resource(RegisterUser, "/register-user")
auth_api.add_resource(Login, "/login")
auth_api.add_resource(Logout, "/logout")
auth_api.add_resource(ChangeRole, "/change-role")
