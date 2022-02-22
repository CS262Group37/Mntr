import os
# We can create multiple config classes in here to easily switch between them
# Remember to change the FLASK_ENV variable in the .env file
class DevConfig:
    SECRET_KEY = 'dev'
    SERVER_NAME = os.getenv('HOSTNAME')

class ProdConfig:
    #SERVER_NAME = 'mydomain.com:5000'
    SECRET_KEY = 'dev' # TODO: Make this a crazy random string for actual deployment
    