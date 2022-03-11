# import sys

# import pytest

<<<<<<< HEAD
# import sys
# sys.path.append('../app')
# from app import create_app

# @pytest.fixture()
# def app():
#     app = create_app()
#     app.config.update({
#         "TESTING": True,
#     })
#     print("created app")
=======
import sys

sys.path.append("../app")
from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    print("created app")
>>>>>>> 483e768c5ab6a7ec3c02e87e88a8fa1a7b947392

#     # other setup can go here

<<<<<<< HEAD
#     yield app
    
#     # clean up / reset resources here
=======
    yield app

    # clean up / reset resources here
>>>>>>> 483e768c5ab6a7ec3c02e87e88a8fa1a7b947392
