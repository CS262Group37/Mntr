from random import randrange
from sys import platform

import os
import names
import requests

roles = ['mentee', 'mentor', 'admin']

def add_user(first_name, last_name, email, password, role):
    print('Adding', first_name, last_name)
    requests.post('http://127.0.0.1:5000/api/auth/register', 
        data={
            'email': email,
            'password': password,
            'firstName': first_name,
            'lastName': last_name,
            'role': role
            }
        )

def add_random_users():
    
    def add_random_user():
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        add_user(first_name, last_name, first_name.lower() + '.' + last_name.lower() + '@gmail.com', 'password', roles[randrange(2)])

    user_count = int(input("Enter the number of random users to add: "))
    for i in range(user_count):
        add_random_user()
    
    add_user(names.get_first_name(), names.get_last_name(), 'admin@gmail.com', 'password', 'admin')
    print("\nAn admin user has been added with email: admin@gmail.com")
    print("All users have password: password")

def add_specific_user():
    first_name = input("\nEnter user's first name: ")
    last_name = input("Enter user's last name: ")
    email = input("Enter user's email: ")
    password = input("Enter user's password: ")
    role = input("Enter user's role: ")

    add_user(first_name, last_name, email, password, role)

# Returns cookies from user login
def login_user(email, password):
    global cookie
    response = requests.post('http://127.0.0.1:5000/api/auth/register', data={'email': email, 'password': password})
    cookie = response.cookies

class Console():
    
    options = {
        '1' : add_random_users,
        '2' : add_specific_user
    }

    def run(self):
        while True:
            self.clear_console()
            option = self.optionSelect()
            self.clear_console()
            self.options[option]()
            input("\nPress any key to continue...")

    def optionSelect(self):
        print("\n1. Add random users")
        print("2. Add specific user")
        return input("\nSelect an option: ")

    def clear_console(self):
        if platform == "linux" or platform == "linux2":
            os.system('clear')
        elif platform == "darwin":
            os.system('clear')
        elif platform == "win32":
            os.system('cls')

if __name__ == "__main__":

    console = Console()
    console.run()
