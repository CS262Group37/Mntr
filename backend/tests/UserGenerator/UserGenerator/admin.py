from time import perf_counter
from random import choice
import json

import requests
from rich.progress import Progress
from rich.prompt import IntPrompt

from .console import hostname, console
from .fake_data import skills, fake
from . import authentication

def add_skill(skill_name):
    
    response = requests.post(f'{hostname}/api/admin/add-skill', data={'skillName': skill_name}, timeout=10, cookies=authentication.active_cookie)
    data = json.loads(response.content)

    if 'error' in data:
        return False
    return True

def add_random_skills():
    skill_count = IntPrompt.ask('Enter the number of random skills to add')

    added_skills = 0
    start = perf_counter()
    with Progress() as progress:
        skill_progress = progress.add_task('[cyan]Adding skills...[/]', total=skill_count)

        for i in range(skill_count):
            skill = choice(skills)
            # Create an account
            if add_skill(skill):
                added_skills += 1
            
            progress.update(skill_progress, advance=1)
    stop = perf_counter()
    console.print(f'\n[green]Successfully added {added_skills} skills in {stop - start} seconds[/]')

def add_topic(topic_name):

    response = requests.post(f'{hostname}/api/admin/add-topic', data={'topicName': topic_name}, timeout=10, cookies=authentication.active_cookie)
    data = json.loads(response.content)

    if 'error' in data:
        return False
    return True

def add_random_topics():
    topic_count = IntPrompt.ask('Enter the number of random topics to add')
    added_topics = 0
    start = perf_counter()
    with Progress() as progress:
        topic_progress = progress.add_task('[cyan]Adding skills...[/]', total=topic_count)

        for i in range(topic_count):
            topic = fake.job()
            # Create an account
            if add_topic(topic):
                added_topics += 1
            
            progress.update(topic_progress, advance=1)
    stop = perf_counter()
    console.print(f'\n[green]Successfully added {added_topics} topics in {stop - start} seconds[/]')

def add_area(area_name):

    response = requests.post(f'{hostname}/api/admin/add-business-area', data={'businessAreaName': area_name}, timeout=10, cookies=authentication.active_cookie)
    data = json.loads(response.content)

    if 'error' in data:
        return False
    return True

def add_random_areas():
    area_count = IntPrompt.ask('Enter the number of random business areas to add')
    add_areas = 0
    start = perf_counter()
    with Progress() as progress:
        area_progress = progress.add_task('[cyan]Adding business areas...[/]', total=area_count)

        for i in range(area_count):
            area = fake.street_address()
            # Create an account
            if add_area(area):
                add_areas += 1
            
            progress.update(area_progress, advance=1)
    stop = perf_counter()
    console.print(f'\n[green]Successfully added {add_areas} business areas in {stop - start} seconds[/]')
