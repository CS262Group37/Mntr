import requests
import json
import random

from rich.table import Table
from rich.progress import Progress
from rich.prompt import IntPrompt
from rich import box

from .console import add_option, console, hostname
from . import authentication
from .database import get_data

def add_meeting(relationID, startTime, endTime, title, description):

    response = requests.post(f'{hostname}/api/meetings/create-meeting',
        data={
            'relationID': relationID,
            'startTime': startTime,
            'endTime': endTime,
            'title': title,
            'description': description
        }, timeout=10
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

    # Get all relations on the system
    relations = get_data('SELECT * FROM relation')
    with Progress() as progress:
        meeting_progress = progress.add_task('[cyan]Adding random meetings...[/]', total=meeting_count)
        
        for i in range(meeting_count):
            relation = random.choice(relations)
            random_time = random.randrange()
            add_meeting(relation, )
