import requests
import json
import random
from datetime import timedelta
from time import perf_counter

from rich.progress import Progress
from rich.prompt import IntPrompt

from .console import add_option, console, hostname
from .authentication import login_user
from . import authentication
from .database import get_data
from .fake_data import fake

def add_meeting(relationID, startTime, endTime, title, description):

    response = requests.post(f'{hostname}/api/meetings/create-meeting',
        data={
            'relationID': relationID,
            'startTime': startTime,
            'endTime': endTime,
            'title': title,
            'description': description
        }, timeout=10, cookies=authentication.active_cookie
        )
    
    data = json.loads(response.content)

    if 'error' in data:
        return False
    return True

def create_random_meetings(meeting_count = None):
    if meeting_count is None:
        meeting_count = IntPrompt.ask('Enter the number of random meetings to add')
        console.line()
    created_meetings = 0
    start = perf_counter()

    # Get all relations on the system
    relations = get_data('SELECT * FROM relation')
    with Progress() as progress:
        meeting_progress = progress.add_task('[cyan]Adding random meetings...[/]', total=meeting_count)
        
        for i in range(meeting_count):
            relation = random.choice(relations)
            # Need to login as relation mentee
            sql = 'SELECT email, password FROM "user" NATURAL JOIN account WHERE "user".userID = %s'
            data = (relation['menteeid'],)
            login_details = get_data(sql, data)
            if not login_user(login_details[0]['email'], login_details[0]['password'], 'mentee'):
                continue
                        
            random_time = fake.date_time_this_century(before_now = False, after_now = True)
            random_end_time = random_time + timedelta(minutes=random.randrange(120))
            if add_meeting(relation, random_time.strftime('%d/%m/%y %H:%M'), random_end_time.strftime('%d/%m/%y %H:%M'), fake.sentences(nb=1), fake.paragraph(nb_sentences=5)):
                created_meetings += 1
            progress.update(meeting_progress, advance=1)
    stop = perf_counter()
    console.print(f'\n[green]Successfully created {created_meetings} meetings in {stop - start} seconds[/]')

def add_options():
    add_option('meetings', 'Add random meetings', create_random_meetings)