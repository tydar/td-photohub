from flask import g, session
from big_picture.models import db
import pytest

def test_hello(client, app):
    assert client.get('/hello').status_code == 200

def test_db_connection(client, app):
    # will throw an error if bad config
    # purely tests that postgres testing setup is reachable
    with app.app_context():
        db.engine.connect()
