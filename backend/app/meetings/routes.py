from app.auth.routes import AuthResource

class create_meeting(AuthResource):
    routes = ['']

    def create():
        return

class cancel_meeting(AuthResource):
    routes = ['']

    def delete():
        return

class accept_meeting(AuthResource):
    routes = ['']

    def accept():
        return
class get_meetings(AuthResource):
    routes = ['']

    def get():
        return 
