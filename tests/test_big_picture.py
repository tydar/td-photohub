from flask import g, session
import pytest

def test_hello(client, app):
    assert client.get('/hello').status_code == 200
