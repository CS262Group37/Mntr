import json
from time import perf_counter

import requests
from rich.progress import track
from rich.prompt import IntPrompt

from . import authentication

from .console import add_option, console
from .fake_data import fake

accounts = {}

class Account():
    def __init__(self, first_name, last_name, email, password):
        self.accountID = -1
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

def create_account(account):

    if account.email in accounts:
        return False

    response = requests.post('http://127.0.0.1:5000/api/auth/register-account', 
        data={
            'email': account.email,
            'password': account.password,
            'firstName': account.first_name,
            'lastName': account.last_name
            }
        )
    
    data = json.loads(response.content)

    if 'error' in data:
        return False

    authentication.active_cookie = response.cookies
    account.accountID = data['accountID']
    accounts[account.email] = account
    return True

def create_random_accounts():
    
    account_count = IntPrompt.ask("Enter the number of random accounts to add")
    created_accounts = 0
    print()
    start = perf_counter()
    for i in track(range(account_count), description="[cyan]Adding random accounts...[/]"):

        account = Account(fake.first_name(), fake.last_name(), fake.email(domain="gmail.com"), fake.sha256())
        
        # Create an account
        if create_account(account):
            created_accounts += 1
            # # Create user
            # random_role = random.randrange(11)
            # if random_role < 5:
            #     create_user(email, 'mentee')
            #     user_count += 1
            # elif random_role < 10:
            #     create_user(email, 'mentor')
            #     user_count += 1
            # else:
            #     create_user(email, 'mentee')
            #     create_user(email, 'mentor')
            #     user_count += 2

    stop = perf_counter()
    console.print(f"\n[green]Successfully added {created_accounts} accounts in {stop - start} seconds[/]")

add_option("Add random accounts", create_random_accounts)
