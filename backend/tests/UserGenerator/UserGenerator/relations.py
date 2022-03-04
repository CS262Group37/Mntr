import json
from random import choice
from time import perf_counter

import requests
from rich import box
from rich.progress import Progress
from rich.prompt import IntPrompt
from rich.table import Table

from . import authentication
from .console import add_option, console, hostname
from .database import get_data


def create_relation(menteeID, mentorID):
    # Get mentee data
    mentee_data = get_data('SELECT * FROM "user" INNER JOIN account ON ("user".accountID = account.accountID) WHERE "user".userID=%s', (menteeID,))
    if not mentee_data:
        return False

    # Login as the mentee
    if not authentication.login_user(mentee_data[0]['email'], mentee_data[0]['password'], mentee_data[0]['role']):
        return False

    response = requests.post(f'{hostname}/api/relations/create-relation', 
        data={
            'mentorID': mentorID
            },
        cookies=authentication.active_cookie, timeout=10
        )
    
    data = json.loads(response.content)

    if 'error' in data:
        return False
    else:
        return True

def add_random_relations(relation_count = None):
    if relation_count is None:
        relation_count = IntPrompt.ask('Enter the number of relations to add')
        console.line()

    # Get mentees in the database
    mentees = get_data('SELECT * FROM "user" WHERE "role"=\'mentee\'')
    mentors = get_data('SELECT * FROM "user" WHERE "role"=\'mentor\'')

    if not mentees or not mentors:
        console.print('[red]The system does not contain enough users to make any relations[/]')
        return
    
    start = perf_counter()

    with Progress() as progress:
        relation_progress = progress.add_task('[cyan]Adding random relations...[/]', total=relation_count)
        added_relations = 0
        for i in range(relation_count):

            # Select a random mentee and mentor
            menteeID = choice(mentees)['userid']
            mentorID = choice(mentors)['userid']

            if create_relation(menteeID, mentorID):
                added_relations += 1
            
            progress.update(relation_progress, advance=1)

    stop = perf_counter()
    console.print(f'\n[green]Successfully added {added_relations} relations in {stop - start} seconds[/]')

def print_all_relations():
    relations = get_data('SELECT * FROM relation;')

    table = Table(title='Relations', box=box.ROUNDED)
    table.add_column('RelationID', justify='center')
    table.add_column('MenteeID', justify='center')
    table.add_column('MentorID', justify='center')

    for row in relations:
        table.add_row(str(row['relationid']), str(row['menteeid']), str(row['mentorid']))

    console.print("Opening relations table in page view")

    with console.pager():
        console.print(table, justify='center')

def print_relations(user_data):
    if user_data[0]['role'] == 'mentee':
        relations = get_data('SELECT * FROM relation INNER JOIN "user" ON relation.mentorID = "user".userID INNER JOIN account ON account.accountID = "user".accountID WHERE relation.menteeID = %s', (user_data[0]['userid'],))
    else:
        relations = get_data('SELECT * FROM relation INNER JOIN "user" ON relation.menteeID = "user".userID INNER JOIN account ON account.accountID = "user".accountID WHERE relation.mentorID = %s', (user_data[0]['userid'],))

    table = Table(title=f'{user_data[0]["firstname"]} {user_data[0]["lastname"]}\'s relations', box=box.ROUNDED)
    table.add_column('RelationID', justify='center')
    table.add_column('UserID', justify='center')
    table.add_column('Role', justify='center')
    table.add_column('First Name', justify='center')
    table.add_column('Last Name', justify='center')

    for row in relations:
        table.add_row(str(row['relationid']), str(row['userid']), str(row['role']), str(row['firstname']), str(row['lastname']))

    console.print(table, justify='center')

def add_options():
    add_option('addr', 'Add random relations', add_random_relations)
    add_option('relations', 'View relations in a table', print_all_relations)
