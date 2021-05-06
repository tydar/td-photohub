import pytest

def test_simple(client, app):
    assert client.get('/search/').status_code == 200

def test_advanced(client, app):
    assert client.get('/search/advanced').status_code == 200
