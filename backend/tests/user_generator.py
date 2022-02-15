from random import randrange

import os
import names
import requests

roles = ['mentee', 'mentor', 'admin']

def add_user(first_name, last_name, email, password, role):
    print("Adding", first_name, last_name)
    requests.post('http://localhost:5000/api/auth/register', 
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

class Console(object):
    
    options = {
        '1' : add_random_users,
        '2' : add_specific_user
    }

    def run(self):
        while True:
            os.system('clear')
            option = self.optionSelect()
            os.system('clear')
            self.options[option]()
            input("\nPress any key to continue...")

    def optionSelect(self):
        print("\n1. Add random users")
        print("2. Add specific user")
        return input("\nSelect an option: ")

if __name__ == "__main__":

    console = Console()
    console.run()
