import json
from random import choice

import requests
from rich import box
from rich.table import Table

from . import console
from . import database
from . import relations
from . import accounts
from . import admin
from . import matching

active_cookie = None
logout_flag = False


def logout(*args):
    global logout_flag
    logout_flag = True


login_options = {
    ("relations", "View relations"): relations.print_relations,
    ("recommendations", "View recommended mentors"): matching.print_recommendations,
    ("logout", "Logout"): logout,
}

admin_options = {
    ("skills", "Add random skills to the system"): admin.add_random_skills,
    ("topics", "Add random topics to the system"): admin.add_random_topics,
    ("areas", "Add random business areas to the system"): admin.add_random_areas,
    ("logout", "Logout"): logout,
}


def login_user(email, password, role):
    response = requests.post(
        f"{console.hostname}/api/auth/login",
        data={"email": email, "password": password, "role": role},
        timeout=10,
    )
    global active_cookie
    active_cookie = response.cookies

    data = json.loads(response.content)
    if "error" in data:
        return False
    return True


def simple_admin_login():
    # Register an admin account and user then login
    accounts.create_account("admin", "admin", "admin@admin.com", "admin")
    accounts.create_user("admin", adminPassword="admin")
    if not login_user("admin@admin.com", "admin", "admin"):
        console.console.print("[red]Admin login failed for an unknown reason[/]")
        return False
    return True


def admin_login():
    global logout_flag
    logout_flag = False

    if simple_admin_login():
        while not logout_flag:
            option = console.select_option(admin_options)
            console.console.line()
            admin_options[option]()
            if not logout_flag:
                console.console.line()


def random_login():
    global logout_flag
    logout_flag = False
    # Select a random account
    accounts = database.get_data("SELECT * FROM account")
    if not accounts:
        console.console.print("[red]There are no accounts on the system[/]")
        return

    random_account = choice(accounts)

    # Select a random user from that account
    users = database.get_data(
        'SELECT * FROM "user" WHERE accountID=%s', (random_account["accountid"],)
    )
    random_user = choice(users)
    if not random_user:
        console.console.print("[red]The selected account does not have any users[/]")
        return

    if login_user(
        random_account["email"], random_account["password"], random_user["role"]
    ):

        user_data = database.get_data(
            'SELECT * FROM account INNER JOIN "user" ON (account.accountID = "user".accountID) WHERE account.accountID=%s',
            (random_account["accountid"],),
        )

        table = Table(title="User Data", box=box.ROUNDED)
        table.add_column("Category", justify="center", style="green")
        table.add_column("Value", justify="center", style="cyan")
        table.add_row("Account ID", str(user_data[0]["accountid"]))
        table.add_row("User ID", str(user_data[0]["userid"]))
        table.add_row("Role", str(user_data[0]["role"]))
        table.add_row("First Name", str(user_data[0]["firstname"]))
        table.add_row("Last Name", str(user_data[0]["lastname"]))
        table.add_row("Email", str(user_data[0]["email"]))
        table.add_row("Password", str(user_data[0]["password"]))
        table.add_row("Profile Picture", str(user_data[0]["profilepicture"]))

        console.console.print(table, justify="center")
        console.console.line()
        console.console.print(
            f"[green]Successfully logged in as [bold]{random_account['firstname']} {random_account['lastname']}[/]"
        )

        while not logout_flag:

            option = console.select_option(login_options)
            console.console.line()
            login_options[option](user_data)
            if not logout_flag:
                console.console.line()


def add_options():
    console.add_option("login", "Login as a random user", random_login)
    console.add_option("admin", "Login as an admin", admin_login)
