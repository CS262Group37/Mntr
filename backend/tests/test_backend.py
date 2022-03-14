from UserGenerator.UserGenerator import accounts
from UserGenerator.UserGenerator import admin
from UserGenerator.UserGenerator import authentication
from UserGenerator.UserGenerator import relations
from UserGenerator.UserGenerator import meetings
from UserGenerator.UserGenerator import console
from UserGenerator.UserGenerator import workshops

from datetime import datetime
import json
import requests

#These are functions used in the tests
#Tests themselves are written further down

def login_user(email, password, role):
    response = requests.post('http://localhost:5000/api/auth/login',
        data={"email": email, "password": password, "role": role},
        timeout=10,
    )
    global active_cookie
    authentication.active_cookie = response.cookies

    data = json.loads(response.content)
    if "error" in data:
        return False
    return True

def create_app_feedback(feedback):
    response = requests.post(
        "http://localhost:5000/api/admin/create-app-feedback",
        data={"content": feedback},
        timeout=10,
        cookies=authentication.active_cookie,
    )
    data = json.loads(response.content)
    print(data)
    if "error" in data:
        return False
    return True

def get_app_feedback():
    response = requests.get(
        "http://localhost:5000/api/admin/get-app-feedback",
        timeout=10,
        cookies=authentication.active_cookie,
    )
    data = json.loads(response.content)
    print(data)
    return True

def add_topic(topic_name):

    response = requests.post("http://localhost:5000/api/admin/add-topic",
        data={"topicName": topic_name},
        timeout=10,
        cookies=authentication.active_cookie,
    )
    data = json.loads(response.content)

    if "error" in data:
        return False
    return True

def add_skill(skill_name):

    response = requests.post("http://localhost:5000}/api/admin/add-skill",
        data={"skillName": skill_name},
        timeout=10,
        cookies=authentication.active_cookie,
    )
    data = json.loads(response.content)

    if "error" in data:
        return False
    return True

def add_area(area_name):

    response = requests.post("http://localhost:5000/api/admin/add-business-area",
        data={"businessAreaName": area_name},
        timeout=10,
        cookies=authentication.active_cookie,
    )
    data = json.loads(response.content)

    if "error" in data:
        return False
    return True

def create_relation(menteeID, mentorID):
    response = requests.post("http://localhost:5000/api/relations/create-relation",
        data={"mentorID": mentorID},
        cookies=authentication.active_cookie,
        timeout=10,
    )

    data = json.loads(response.content)

    if "error" in data:
        return False
    else:
        return True

def str_to_datetime(str):
    """Convert provided string to a datetime object.

    String format must be %d/%m/%y %H:%M.
    Returns False if conversion fails.
    """
    try:
        datetime_object = datetime.strptime(str, "%d/%m/%y %H:%M")
    except:
        return False
    else:
        return datetime_object

def accept_meeting(meeting_ID):
    response = requests.post("http://localhost:5000/api/relations/accept-meeting",
        data = {
            'meetingID': meeting_ID
        },
        cookies=authentication.active_cookie,
        timeout=10
    )
    return True


def rate_mentor(mentor_id,skills,rating):
    response = requests.post("http://localhost:5000/api/relations/rate-mentor",
        data = {
            'mentorID': mentor_id,
            'skills': skills,
            'rating': rating
        },
        cookies=authentication.active_cookie,
        timeout=10
    )
    data = json.loads(response.content)
    if 'error' in data:
        return False
    return True

def send_email(recipient_id,subject,content):
    response = requests.post("http://localhost:5000/api/relations/send-email",
        data = {
            'recipientID': recipient_id,
            'subject': subject,
            'content': content
        },
        cookies = authentication.active_cookie,
        timeout=10
    )
    data = json.loads(response.content)
    if 'error' in data:
        return False
    return True
    

def join_workshop(workshop_id):
    response = requests.post("http://localhost:5000/api/relations/send-email",
        data = {
            'workshopID': workshop_id
        },
        cookies=authentication.active_cookie,
        timeout=10
    )
    data = json.loads(response.content)
    if 'error' in data:
        return False
    return True






# Where backend tests will be written

mentee_id = 2
mentor_id = 3

def test_adminFunctions():
    #Login as admin
    accounts.create_account('admin','admin','admin@admin.com','admin')
    accounts.create_user('admin',adminPassword='admin')
    login_user('admin@admin.com','admin','admin')

    #D12
    assert admin.add_topic('Investments') is True
    assert admin.add_area('Trading') is True
    assert admin.add_area('Customer service') is True

    #D10
    assert admin.add_skill('Listening') is True

def test_createAccount():
    #C2/D2
    #Create mentee user
    assert accounts.create_account('Mentee','Mentee','mentee@mentee.com','password') is True
    assert accounts.create_user('mentee','Customer service','Investments','Listening','7','admin') is True


    #Create mentor user
    assert accounts.create_account('Mentor','Mentor','mentor@mentor.com','password') is True
    assert accounts.create_user('mentor','Trading','Investments',adminPassword='admin') is True

def test_adminFunctionsForUsers():
    #Test if a mentee can add business areas, topics or skills
    login_user('mentee@mentee.com','password','mentee')
    assert admin.add_area('Area') is False
    assert admin.add_topic('Topic') is False
    assert admin.add_skill('Skill') is False
    
    #Test if a mentor can add business areas, topics or skills
    login_user('mentor@mentor.com','password','mentor')
    assert admin.add_area('Area') is False
    assert admin.add_topic('Topic') is False
    assert admin.add_skill('Skill') is False

def test_createRelation():
    #Create mentee/mentor relation between mentor and mentee from different business areas
    assert relations.create_relation(mentee_id,mentor_id) is True

    #Create mentee user with same business area as mentor user
    accounts.create_account('Mentee2','Mentee2','menteetwo@menteetwo.com','password')
    accounts.create_user('mentee','Trading','Investments','Listening','7',adminPassword='admin')
    #Test if relation can be made between mentee and mentor from same business area
    #D4
    assert relations.create_relation(4,mentor_id) is False

def test_rateMentor():
    #Add skill as admin
    login_user('admin@admin.com','admin','admin')
    admin.add_skill('Patience')
    #Login as mentee
    login_user('mentee@mentee.com','password','mentee')

    #Rate mentor
    #C10
    assert rate_mentor(3,['Listening','Patience'],[2,7]) is True

def test_sendEmail():
    #C17
    assert send_email(3,'Test email','This is a test email') is True

def test_createWorkshop():
    login_user('mentor@mentor.com','password','mentor')
    #Create workshop as a mentor
    #C9
    assert workshops.add_workshop(3,'Test workshop','Investments','Testing add workshop function','12/10/21 10:00','12/10/21 11:00','Anywhere') is True

    login_user('mentee@mentee.com','password','mentee')
    #Try create a workshop as a mentee
    #C9
    assert workshops.add_workshop(2,'Test workshop','Investments','Testing add workshop function','12/10/21 10:00','12/10/21 11:00','Anywhere') is False

def test_joinWorkshopAsMentee():
    #Join workshop as a mentee
    assert join_workshop(1) is True

def test_createMeeting():
    #Login as mentee
    assert login_user('mentee@mentee.com','password','mentee') is True
    #Test if mentee can request meeting with mentor
    assert meetings.add_meeting(1,'13/10/21 10:00','13/10/21 11:00','Stuff','Doing stuff') is True

def test_acceptMeetingAsMentor():
    #Test if mentor can accept meeting
    assert accept_meeting(1) is True

def test_addingAppFeedback():
    #Add app feedback as a mentee
    create_app_feedback('Good app')

def test_gettingAppFeedback():
    #Login as admin
    login_user('admin@admin.com','admin','admin')
    #D11
    assert get_app_feedback() is True