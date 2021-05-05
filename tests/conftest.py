import pytest
from big_picture import create_app

@pytest.fixture
def app():
    # set up DB here later
    app = create_app({'TESTING': True,})

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
