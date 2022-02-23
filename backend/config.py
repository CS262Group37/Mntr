import os
from dotenv import load_dotenv

load_dotenv()

# We can create multiple config classes in here to easily switch between them
# Remember to change the FLASK_ENV variable in the .env file
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'cookie',
        'name': 'JTW_Token'
    }
}
class DevConfig:
    SECRET_KEY = 'dev'
    RESTX_VALIDATE = True
    if os.getenv('HOSTNAME')[7:] != '127.0.0.1:5000' and os.getenv('HOSTNAME')[7:] != 'localhost':
        SERVER_NAME = os.getenv('HOSTNAME')[7:]
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_UI_DOC_EXPANSION = 'list'

class ProdConfig:
    #SERVER_NAME = 'mydomain.com:5000'
    SECRET_KEY = 'dev' # TODO: Make this a crazy random string for actual deployment
    