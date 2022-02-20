from time import perf_counter

import random
import sys
import getopt
import os
import names
import requests
import json

roles = ['mentee', 'mentor', 'admin']

accounts = {}
mentors = {}
mentees = {}
admins = {}

class Account():
    def __init__(self, accountID, firstName, lastName):
        self.accountID = accountID
        self.firstName = firstName
        self.lastName = lastName

def create_account(first_name, last_name, email, password):
    if email in accounts:
        return False

    response = requests.post('http://127.0.0.1:5000/api/auth/register-account', 
        data={
            'email': email,
            'password': password,
            'firstName': first_name,
            'lastName': last_name
            }
        )
    data = json.loads(response.content)
    if 'error' in data:
        print("Returning false")
        return False
    global active_cookie
    active_cookie = response.cookies
    accounts[email] = Account(data['accountID'], first_name, last_name)
    return True

def create_user(email, role):

    response = requests.post('http://127.0.0.1:5000/api/auth/register-user', 
        data={
            'role': role
            },
        cookies=active_cookie
        )
    data = json.loads(response.content)
    
    if role == 'mentor':
        mentors[email] = data['userID']
    elif role == 'mentee':
        mentees[email] = data['userID']
    else:
        admins[email] = data['userID']

# Print iterations progress from https://stackoverflow.com/a/34325723
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def create_random_accounts():
    
    user_count = 0
    account_count = int(input("Enter the number of random accounts to add: "))
    print()
    start = perf_counter()
    for i in range(account_count):
        
        if use_real_names:
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            email = first_name.lower() + '.' + last_name.lower() + str(random.randrange(1000)) + '@gmail.com'
        else:
            first_name = str(random.randrange(1000))
            last_name = str(random.randrange(1000))
            email = first_name + '.' + last_name + str(random.randrange(1000)) + '@gmail.com'

        # Create an account
        if create_account(first_name, last_name, email, 'password'):
            
            # Create user
            random_role = random.randrange(11)
            if random_role < 5:
                create_user(email, 'mentee')
                user_count += 1
            elif random_role < 10:
                create_user(email, 'mentor')
                user_count += 1
            else:
                create_user(email, 'mentee')
                create_user(email, 'mentor')
                user_count += 2
        else:
            account_count -= 1

        printProgressBar(i + 1, account_count, prefix='Progress:', suffix='Complete', length=50)
    stop = perf_counter()
    create_account(names.get_first_name(), names.get_last_name(), 'admin@gmail.com', 'password')
    create_user('admin@gmail.com', 'admin')
    print("\nAn admin account has been added with email: admin@gmail.com")
    print("All users have password: password")
    print("\nSuccessfully added", account_count + 1, "accounts with a total of", user_count + 1, "users\nTook", stop-start, "seconds")

def create_relation(mentee_email, mentor_email):

    # Login as the mentee
    login_user(mentee_email, 'password', 'mentee')

    response = requests.post('http://127.0.0.1:5000/api/relations/create-relation', 
        data={
            'mentorID': mentors[mentor_email]
            },
        cookies=active_cookie
        )
    
    data = json.loads(response.content)
    if 'error' in data:
        return False
    else:
        return True


def create_random_relations():

    relation_count = int(input("Enter the number of relations to create: "))
    print()
    if len(accounts) == 0:
        print("\nThe system does not contain any users")
        return
    
    start = perf_counter()
    success_count = 0
    for i in range(relation_count):

        # Select a random mentee and mentor
        mentee_email = random.choice(list(mentees.keys()))
        mentor_email = random.choice(list(mentors.keys()))

        if create_relation(mentee_email, mentor_email):
            success_count += 1
        
        printProgressBar(i + 1, relation_count, prefix='Progress:', suffix='Complete', length=50)

    stop = perf_counter()
    print("\nSuccessfully created", success_count, "relations\nTook", stop-start, "seconds")

def random_login():

    if len(accounts) == 0:
        print("Cannot login, there are no users on the system")
        return
    
    random_email = random.choice(list(accounts.keys()))
    if random_email in mentors and random_email in mentees:
        r = random.randrange(2)
        role = roles[r]
    if random_email in mentors:
        role = 'mentor'
    else:
        role = 'mentee'

    login_user(random_email, 'password', role)
    print("Logged in as", accounts[random_email].firstName, accounts[random_email].lastName, "with role", role)

# Returns cookies from user login
def login_user(email, password, role):
    response = requests.post('http://127.0.0.1:5000/api/auth/login', data={'email': email, 'password': password, 'role': role})
    global active_cookie
    active_cookie = response.cookies

class Console():
    
    options = {
        '1' : create_random_accounts,
        '2' : create_random_relations,
        '3' : random_login,
        'q' : exit
    }

    def run(self):
        while True:
            self.clear_console()
            option = self.optionSelect()
            self.clear_console()
            self.options[option]()
            input("\nPress enter to continue...")

    def optionSelect(self):
        print("\n1. Add random accounts")
        print("2. Create random relations")
        print("3. Login as random user")
        print("\nType q to exit")
        return input("\nSelect an option: ")

    def clear_console(self):
        if sys.platform == "linux" or sys.platform == "linux2":
            os.system('clear')
        elif sys.platform == "darwin":
            os.system('clear')
        elif sys.platform == "win32":
            os.system('cls')

if __name__ == "__main__":

    global use_real_names
    use_real_names = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'n', ['names'])
    except:
        print("Error")
  
    for opt, arg in opts:
        if opt in ('-n', '--names'):
            use_real_names = True

    console = Console()
    console.run()
