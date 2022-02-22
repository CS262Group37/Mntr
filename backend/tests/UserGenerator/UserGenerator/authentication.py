import json
from random import choice

import requests
from rich import box
from rich.table import Table

from .console import add_option, console, select_option
from .database import get_data
from .relations import print_relations

active_cookie = None
logout_flag = False

def logout(*args):
    global logout_flag
    logout_flag = True

options = {
    'View relations': print_relations,
    'Logout': logout
}

def login_user(email, password, role):
    response = requests.post('http://127.0.0.1:5000/api/auth/login', data={'email': email, 'password': password, 'role': role}, timeout=10)
    global active_cookie
    active_cookie = response.cookies

    data = json.loads(response.content)
    if 'error' in data:
        return False
    return True

def random_login():
    global logout_flag
    logout_flag = False
    # Select a random account
    accounts = get_data('SELECT * FROM account')
    if not accounts:
        console.print("[red]There are no accounts on the system[/]")
        return
    
    random_account = choice(accounts)
    
    # Select a random user from that account
    users = get_data('SELECT * FROM "user" WHERE accountID=%s', (random_account['accountid'],))
    random_user = choice(users)
    if not random_user:
        console.print("[red]The selected account does not have any users[/]")
        return

    if login_user(random_account['email'], random_account['password'], random_user['role']):
        
        user_data = get_data('SELECT * FROM account INNER JOIN "user" ON (account.accountID = "user".accountID) WHERE account.accountID=%s', (random_account['accountid'],))

        table = Table(title='User Data', box=box.ROUNDED)
        table.add_column('Category', justify='center', style='green')
        table.add_column('Value', justify='center', style='cyan')
        table.add_row('Account ID', str(user_data[0]['accountid']))
        table.add_row('User ID', str(user_data[0]['userid']))
        table.add_row('Role', str(user_data[0]['role']))
        table.add_row('First Name', str(user_data[0]['firstname']))
        table.add_row('Last Name', str(user_data[0]['lastname']))
        table.add_row('Email', str(user_data[0]['email']))
        table.add_row('Password', str(user_data[0]['password']))

        console.print(table, justify="center")
        console.line()
        console.print(f"[green]Successfully logged in as [bold]{random_account['firstname']} {random_account['lastname']}[/]")
        
        while not logout_flag:
            
            option = select_option(options)
            console.line()
            options[option](user_data)
            if not logout_flag:
                console.line()

def add_options():
    add_option("Login as random user", random_login)
