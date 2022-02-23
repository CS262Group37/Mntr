import os

from rich import box
from rich.console import Console
from rich.prompt import PromptBase
from rich.table import Table
from dotenv import load_dotenv

console = Console()
load_dotenv()
hostname = os.getenv('HOSTNAME')

options = {}

class OptionPrompt(PromptBase[str]):
    response_type = str
    illegal_choice_message = (
        "[prompt.invalid.choice]Please enter one of the available commands"
    )

def add_option(command, description, function):
    options[(command, description)] = function

def select_option(options):
    # Print options
    table = Table(title='Options', box=box.ROUNDED)
    table.add_column('Command', justify='center', style='green')
    table.add_column('Description', justify='center', style='cyan')

    optionsList = list(options.keys())
    choices = []
    for option in optionsList:
        table.add_row(option[0], option[1])
        choices.append(option[0])
    console.print(table, justify='center')

    # Option input
    option = OptionPrompt.ask('\n[orange]Enter a command[/]', choices=choices, show_choices=False)
    for o in optionsList:
        if o[0] == option:
            option = o
            break
    return option

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
    