import os

# We can create multiple config classes in here to easily switch between them
# Remember to change the FLASK_ENV variable in the .env file
class DevConfig:
    DEBUG = True
    SECRET_KEY = 'dev'

class ProdConfig:
    DEBUG = False

APP_ROOT = os.path.dirname(os.path.abspath(__file__))