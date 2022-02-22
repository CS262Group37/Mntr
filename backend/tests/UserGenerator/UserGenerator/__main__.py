from rich.traceback import install

from UserGenerator import (accounts, authentication, console, database, relations)

install(show_locals=True)
database.create_connection()
accounts.add_options()
relations.add_options()
authentication.add_options()
console.add_option("Quit", database.exit_program)
console.run()
