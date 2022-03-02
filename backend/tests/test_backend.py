# from app.admin import admin
# from app.auth import auth
# from app.matching import matching
# from app.meetings import meetings
# from app.messages import messages
# from app.planOfAction import planOfAction
# from app.relations import relations

import json
import requests

# Where backend tests will be written

def create_account(first_name, last_name, email, password):
    response = requests.post('http://localhost:5000/api/auth/register-account', 
        data={
            'email': email,
            'password': password,
            'firstName': first_name,
            'lastName': last_name
            }, timeout=10
        )
    
    data = json.loads(response.content)
    print(data)
    if 'error' in data:
        return False

    return True

def test_backend():

    print("Testing create account")
    assert create_account('Joshua', 'Manchester', 'test@gmail.com', 'password') is True

    # # C1
    # assert admin.add_topic() is 
    # # C2
    # assert admin.add_topic() is 
    # # C3
    # assert admin.add_topic() is 
    # # C4
    # assert admin.add_topic() is 
    # # C5
    # assert admin.add_topic() is 
    # # C6
    # assert admin.add_topic() is 
    # # C7
    # assert admin.add_topic() is 
    # # C8
    # assert admin.add_topic() is 
    # # C9
    # assert admin.add_topic() is 
    # # C10
    # assert admin.add_topic() is 
    # # C11
    # assert admin.add_topic() is 
    # # D12
    # assert admin.add_topic() is 
    # # C13
    # assert admin.add_topic() is 