import sys

import pytest

import sys
sys.path.append('../app')
from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    print("created app")

    # other setup can go here

    yield app
    
    # clean up / reset resources here
