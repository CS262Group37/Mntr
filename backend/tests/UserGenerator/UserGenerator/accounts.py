import json
from random import randrange, choice, sample
from time import perf_counter

import requests
from rich import box
from rich.progress import Progress
from rich.prompt import IntPrompt
from rich.table import Table

from . import authentication, database
from .console import add_option, console, hostname
from .fake_data import fake

def create_account(first_name, last_name, email, password):
    response = requests.post(f'{hostname}/api/auth/register-account', 
        data={
            'email': email,
            'password': password,
            'firstName': first_name,
            'lastName': last_name
            }, timeout=10
        )
    
    data = json.loads(response.content)

    if 'error' in data:
        return False

    authentication.active_cookie = response.cookies
    return True

def print_all_accounts():
    accounts = database.get_data('SELECT * FROM account;')

    table = Table(title='Accounts', box=box.ROUNDED)
    table.add_column('AccountID', justify='center')
    table.add_column('First Name', justify='center')
    table.add_column('Last Name', justify='center')
    table.add_column('Email', justify='center')
    table.add_column('Password', justify='center')
    
    for row in accounts:
        table.add_row(str(row['accountid']), str(row['firstname']), str(row['lastname']), str(row['email']), str(row['password']))

    console.print("Opening accounts table in page view")

    with console.pager():
        console.print(table, justify='center')

def create_user(role, businessArea = None, topics = None, skills = None, ratings = None, adminPassword = None):

    if role == 'admin':
        data = {
            'role': role,
            'adminPassword': adminPassword
        }
    elif role == 'mentor':
        data = {
            'role': role,
            'businessArea': businessArea,
            'topics': topics,
        }
    else:
        data = {
            'role': role,
            'businessArea': businessArea,
            'topics': topics,
            'skills': skills,
            'ratings': ratings,
        }

    response = requests.post(f'{hostname}/api/auth/register-user', data, cookies = authentication.active_cookie, timeout=10)
    data = json.loads(response.content)
    if 'error' in data:
        console.print(data['error'])
        return False
    return True

def print_all_users():
    users = database.get_data('SELECT * FROM "user";')

    table = Table(title='Users', box=box.ROUNDED)
    table.add_column('UserID', justify='center')
    table.add_column('AccountID', justify='center')
    table.add_column('Role', justify='center')

    for row in users:
        table.add_row(str(row['userid']), str(row['accountid']), str(row['role']))

    console.print("Opening users table in page view")

    with console.pager():
        console.print(table, justify='center')

def create_random_accounts_and_users():
    account_count = IntPrompt.ask('Enter the number of random accounts to add')
    created_accounts = 0
    created_users = 0
    console.line()
    start = perf_counter()

    def remove_tuples(list):
        newList = []
        for item in list:
            newList.append(item[0])
        return newList

    def random_ratings(skills):
        ratings = []
        for i in range(len(skills)):
            ratings.append(randrange(11))
        return ratings

    # Get data on the system
    businessAreas = remove_tuples(database.get_data('SELECT "name" FROM system_business_area'))
    skills = remove_tuples(database.get_data('SELECT "name" FROM system_skill'))
    topics = remove_tuples(database.get_data('SELECT "name" FROM system_topic'))

    if not businessAreas or not skills or not topics:
        console.print('[red]System is missing either business areas, skills or topics[/]')
        return

    with Progress() as progress:
        account_progress = progress.add_task('[cyan]Adding random accounts and users...[/]', total=account_count)

        for i in range(account_count):

            # Create an account
            if create_account(fake.first_name(), fake.last_name(), fake.ascii_company_email(), fake.sha256()[10:]):

                created_accounts += 1

                # Create random user(s)
                random_role = randrange(11)
                if random_role < 5:
                    if create_user('mentee', businessArea=choice(businessAreas), topics=sample(topics, k=randrange(1, len(topics))), skills=skills, ratings=random_ratings(skills)) : created_users += 1
                elif random_role < 10:
                    if create_user('mentor', businessArea=choice(businessAreas), topics=sample(topics, k=randrange(1, len(topics)))) : created_users += 1
                else:
                    if create_user('mentee', businessArea=choice(businessAreas), topics=sample(topics, k=randrange(1, len(topics))), skills=skills, ratings=random_ratings(skills)) : created_users += 1
                    if create_user('mentor', businessArea=choice(businessAreas), topics=sample(topics, k=randrange(1, len(topics)))) : created_users += 1
            
            progress.update(account_progress, advance=1)

    stop = perf_counter()
    console.print(f'\n[green]Successfully added {created_accounts} accounts with {created_users} users in {stop - start} seconds[/]')

def add_options():
    add_option('add', 'Add random accounts and users', create_random_accounts_and_users)
    add_option('users', 'View users in a table', print_all_users)
    add_option('accounts', 'View accounts in a table', print_all_accounts)
