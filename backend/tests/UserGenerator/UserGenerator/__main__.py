from rich.traceback import install

from UserGenerator import console
from UserGenerator import database
from UserGenerator import accounts
from UserGenerator import authentication
from UserGenerator import relations
from UserGenerator import meetings

install(show_locals=True)
database.create_connection()
accounts.add_options()
relations.add_options()
authentication.add_options()
meetings.add_options()
console.add_option('exit', 'Exit', database.exit_program)
console.run()
