import requests
import json

from rich.table import Table
from rich import box

from .console import add_option, console, hostname
from . import authentication
from .database import get_data

def print_recommendations(user_data):
    if user_data[0]['role'] != 'mentee':
        console.print('[red]Can only get recommendations for mentors[/]')
        return

    response = requests.get(f'{hostname}/api/matching/relation-recommendations', cookies=authentication.active_cookie, timeout=10)

    data = json.loads(response.content)

    table = Table(title=f'{user_data[0]["firstname"]} {user_data[0]["lastname"]}\'s recommendations', box=box.ROUNDED)
    table.add_column('Mentor Name', justify='center')
    table.add_column('UserID', justify='center')
    table.add_column('Topics', justify='center')
    table.add_column('Ratings', justify='center')
    table.add_column('Compatibility Factor', justify='center')

    for dict in data:
        mentorAccount = get_data('SELECT * FROM "user" INNER JOIN account ON ("user".accountID = account.accountID) WHERE "user".userID=%s', (dict['userID'],))
        mentorTopics = get_data('SELECT * FROM "user_topic" WHERE userID=%s', (dict['userID'],))
        mentorRatings = get_data('SELECT * FROM "user_rating" WHERE userID=%s', (dict['userID'],))
        topics = []
        for mentorTopic in mentorTopics:
            topics.append(mentorTopic['topic'])

        ratings = []
        for mentorRating in mentorRatings:
            ratings.append((mentorRating['skill'], mentorRating['rating']))

        table.add_row(f"{mentorAccount[0]['firstname']} {mentorAccount[0]['lastname']}", str(dict['userID']), str(topics), str(ratings), str(dict['compatibility']))

    console.print(table, justify='center')