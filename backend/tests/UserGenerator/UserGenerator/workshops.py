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
from .database import get_data, update_data
from .fake_data import fake


def add_workshop(mentorID, title, topic, description, startTime, endTime, location):

    response = requests.post(
        f"{hostname}/api/workshop/create-workshop",
        data={
            "mentorID": mentorID,
            "title": title,
            "topic": topic,
            "desc": description,
            "startTime": startTime,
            "endTime": endTime,
            "location": location,
        },
        timeout=10,
        cookies=authentication.active_cookie,
    )

    data = json.loads(response.content)

    if "error" in data:
        return False
    return True


def create_random_workshops(workshop_count=None):
    if workshop_count is None:
        workshop_count = IntPrompt.ask("Enter the number of random workshops to add")
        console.line()
    created_workshops = 0
    start = perf_counter()

    # Get all mentors on the system
    mentors = get_data('SELECT * FROM "user" WHERE "role" = \'mentor\'')
    with Progress() as progress:
        workshop_progress = progress.add_task(
            "[cyan]Adding random workshops...[/]", total=workshop_count
        )

        for i in range(workshop_count):
            mentor = random.choice(mentors)
            sql = 'SELECT email, password FROM "user" NATURAL JOIN account WHERE "user".userID = %s'
            data = (mentor["userid"],)
            login_details = get_data(sql, data)
            if not login_user(
                login_details[0]["email"], login_details[0]["password"], "mentor"
            ):
                continue

            random_time = fake.date_time_this_century(before_now=False, after_now=True)
            random_end_time = random_time + timedelta(minutes=random.randrange(120))

            # Get the mentor's topics
            sql = "SELECT topic FROM user_topic WHERE userID = %s;"
            topics = get_data(sql, (mentor["userid"],))
            random_topic = random.choice(topics)["topic"]

            if add_workshop(
                mentor["userid"],
                fake.sentences(nb=1),
                random_topic,
                fake.paragraph(nb_sentences=5),
                random_time.strftime("%d/%m/%y %H:%M"),
                random_end_time.strftime("%d/%m/%y %H:%M"),
                fake.address(),
            ):
                created_workshops += 1
            progress.update(workshop_progress, advance=1)
    stop = perf_counter()
    console.print(
        f"\n[green]Successfully created {created_workshops} workshops in {stop - start} seconds[/]"
    )


def add_options():
    add_option("workshops", "Add random workshops", create_random_workshops)
