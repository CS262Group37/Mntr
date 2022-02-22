import os

from rich import box
from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table
from dotenv import load_dotenv

console = Console()
load_dotenv()
hostname = os.getenv('API_HOSTNAME')

options = {}

def add_option(name, function):
    print("Adding", name)
    options[name] = function

def select_option(options):
    # Print options
    table = Table(title='Options', box=box.ROUNDED)
    table.add_column('Number', justify='center', style='green')
    table.add_column('Name', justify='center', style='cyan')

    i = 0
    optionsList = list(options.keys())
    choices = []
    for option in optionsList:
        i += 1
        table.add_row(str(i), option)
        choices.append(str(i))
    console.print(table, justify='center')

    # Option input
    option = IntPrompt.ask('\n[orange]Select an option[/]', choices=choices, show_choices=False)

    return optionsList[option - 1]

def execute_option(option):
    console.line(2)
    if options[option].__name__ == 'exit_program':
        console.rule('[red bold]Exiting program 🚪[/]')
        console.line(2)
        options[option]()
    console.rule('[green bold]Option launched ✅[/]')
    console.line(2)

    options[option]()

    console.line(2)
    console.rule('[red bold]Option closed ❌[/]')
    console.line(2)

def run():
    console.clear()
    console.rule('[bold]🎲 User Generator 🎲[/]')
    console.line()
    while True:
        option = select_option(options)
        execute_option(option)
    