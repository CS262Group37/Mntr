# from app.admin import admin
# from app.auth import auth
# from app.matching import matching
# from app.messages import messages
# from app.planOfAction import planOfAction
# from app.relations import relations


from http import cookies
from UserGenerator.UserGenerator import accounts
from UserGenerator.UserGenerator import admin
from UserGenerator.UserGenerator import authentication

from datetime import datetime
import json
import requests

# Where functions used in testing are written

# def register_account(first_name, last_name, email, password):
#     response = requests.post('http://localhost:5000/api/auth/register-account', 
#         data={
#             'email': email,
#             'password': password,
#             'firstName': first_name,
#             'lastName': last_name
#             }, timeout=10
#         )
    
#     data = json.loads(response.content)
#     print(data)
#     if 'error' in data:
#         return False
#     global active_cookie
#     active_cookie = response.cookies
#     return True

# def register_user(role, business_area, topics, skills, ratings):
#     response = requests.post('http://localhost:5000/api/auth/register-user',
#         data ={
#             'role': role,
#             'businessArea': business_area,
#             'topics': topics,
#             'skills': skills,
#             'ratings': ratings,
#             'adminPassword': 'admin'
#         },
#         cookies = active_cookie,
#         timeout=10
#     )
#     data = json.loads(response.content)
#     print(data)
#     if 'error' in data:
#         return False
#     return True

# def login():

# def create_relation(mentee_ID, mentor_ID):
#     reponse = requests.post('http://localhost:5000/api/meetings/create-meeting',
#         data ={
#             'menteeID': mentee_ID,
#             'mentorID': mentor_ID
#         }, timeout=10
#     )
#     data = json.loads(reponse.content)
#     print(data)
#     if 'error' in data:
#         return False
#     return True

# def request_meeting(relation_ID, start_time, end_time, title, description):
#     response = requests.post('http://localhost:5000/api/meetings/create-meeting',
#         data ={
#             'relationID': relation_ID,
#             'startTime': start_time,
#             'endTime': end_time,
#             'title': title,
#             'description': description
#         }, timeout=10
#     )

#     data = json.loads(response.content)
#     print(data)
#     if 'error' in data:
#         return False
#     return True

# def getRecommendedMentors(menteeID):
#     response = requests.post('http://localhost:5000/api/matching/relation-recommendations',
#         data = {
#             'menteeID': menteeID
#             }, timeout=10
#     )

#     data = json.loads(response.content)
#     print(data)
#     if 'error' in data:
#         return False
#     return True


# def add_topic(topic):
#     response = requests.post('http://localhost:5000/api/admin/add-topic',
#         data = {
#             'topicName': topic
#         }, 
#         timeout=10,
#         cookies = active_cookie
#     )

#     data = json.loads(response.content)
#     print(data)
#     if 'error' in data:
#         return False
#     return True

def remove_topic(topic):
    response = requests.post('http://localhost:5000/api/admin/remove-topic',
        data = {
            'topicName': topic
        }, 
        cookies = authentication.active_cookie,
        timeout=10
    )

    data = json.loads(response.content)
    print(data)
    if 'error' in data:
        return False
    return True

def remove_skill(skill):
    response = requests.post('http://localhost:5000/api/admin/remove-skill',
        data = {
            'skillName': skill
        }, 
        cookies = authentication.active_cookie,
        timeout=10
    )

    data = json.loads(response.content)
    print(data)
    if 'error' in data:
        return False
    return True

def remove_area(business_area):
    response = requests.post('http://localhost:5000/api/admin/remove-business-area',
        data = {
            'businessArea': business_area
        }, 
        cookies = authentication.active_cookie,
        timeout=10
    )

    data = json.loads(response.content)
    print(data)
    if 'error' in data:
        return False
    return True

def create_app_feedback(feedback):
    response = requests.post('http://localhost:5000/api/admin/create-app-feedback',
        data = {
            'content': feedback
        }, 
        timeout = 10,
        cookies=authentication.active_cookie
    )
    data = json.loads(response.content)
    print(data)
    if 'error' in data:
        return False
    return True

def get_app_feedback():
    response = requests.get('http://localhost:5000/api/admin/get-app-feedback',
    timeout = 10,
    cookies=authentication.active_cookie
    )
    data = json.loads(response.content)
    print(data)
    if 'error' in data:
        return False
    return True

def login_as_admin():
    response = requests.post('http://localhost:5000/api/auth/login',
        data = {
            'email': 'admin@admin.com',
            'password': 'admin'
        },
        timeout = 10
    )
    data = json.loads(response.content)
    print(data)
    if 'error' in data:
        return False
    return True

# def add_business_area(business_area):
#     response = requests.post('http://localhost:5000/api/admin/add-business-area',
#         data = {
#             'businessAreaName': business_area
#             }, timeout=10
#     )

#     data = json.loads(response.content)
#     print(data)
#     if 'error' in data:
#         return False
#     return True

# def remove_business_area(business_area):
#     response = requests.post('http://localhost:5000/api/admin/remove-business-area',
#         data = {
#             'businessAreaName': business_area
#             }, timeout=10
#     )

#     data = json.loads(response.content)
#     print(data)
#     if 'error' in data:
#         return False
#     return True


# def test_userGenerator():
#     accounts.load_preset()


# Where backend tests will be written


def test_admin_properties():
    #Create and log in to admin account
    authentication.simple_admin_login()

    #D12
    assert admin.add_topic('Investments') is True
    #assert remove_topic('Investments') is True
    assert admin.add_area('Trading') is True
    assert remove_area('Trading') is True
    assert admin.add_skill('Listening') is True
    assert remove_skill('Listening') is True

    accounts.create_account('John','Doe','test@gmail.com','password')
    accounts.create_user('mentee')
    create_app_feedback('Good app')
    login_as_admin()
    #D11
    assert get_app_feedback() is True

    



def test_creating_account():

    # C2
    print("Testing create account")
    assert accounts.create_account('John', 'Smith', 'test@gmail.com', 'password') is True
    assert accounts.create_account('Henry','Willis','email@gmail.com','password') is True
    #assert register_user(mentor,) is True

# def test_create_meeting():

#     # C6
#     startTime = str_to_datetime(10)
#     print(startTime)
#     print("Testing create meeting")
#     assert request_meeting('123456','10/03/2022  19:59','11/03/2022  20:02','Test Meeting','Testing create meeting function') is True

def test_get_recommended_mentors():
    
    # C3 not done
    print("Testing getting recommended mentors")

    #

