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
from .fake_data import fake

def add_plan(relationID, title, description):
    response = requests.post(f'{hostname}/api/plan/add-plan', 
        data={
            'relationID': relationID,
            'title': title,
            'description': description
            }, timeout=10, cookies = authentication.active_cookie
        )
    
    data = json.loads(response.content)

    if 'error' in data:
        print(data)
        return False

    authentication.active_cookie = response.cookies
    return True

def add_random_plans(plan_count = None):
    if plan_count is None:
        plan_count = IntPrompt.ask('Enter the number of plans to add')
        console.line()
    
    # Get relations in the database
    relations = get_data('SELECT * FROM relation')

    if not relations:
        console.print('[red]The system does not contain enough relations to add any plans[/]')
        return

    start = perf_counter()
    with Progress() as progress:
        plan_progress = progress.add_task('[cyan]Adding random relations...[/]', total=plan_count)
        added_plans = 0
        for i in range(plan_count):

            # Select a random relations
            random_relation = choice(relations)

            # Get mentee data
            mentee_data = get_data('SELECT * FROM "user" INNER JOIN account ON ("user".accountID = account.accountID) WHERE "user".userID=%s', (random_relation['menteeid'],))
            
            # Login as the mentee
            if not authentication.login_user(mentee_data[0]['email'], mentee_data[0]['password'], mentee_data[0]['role']):
                continue
            
            # Add the plan
            if add_plan(random_relation['relationid'], fake.sentences(nb=1), fake.sentences(nb=5)):
                added_plans += 1
            
            progress.update(plan_progress, advance=1)
    stop = perf_counter()
    console.print(f'\n[green]Successfully added {added_plans} plans of action in {stop - start} seconds[/]')

def add_options():
    add_option('plan', 'Add random plans of action', add_random_plans)
