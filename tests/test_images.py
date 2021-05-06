import pytest

def test_hello(client, app):
    assert client.get('/hello').status_code == 200

def test_gallery(client, app):
    assert client.get('/images').status_code == 200

def test_add(client, app):
    assert client.get('/images/add').status_code == 200

def test_details(client, app):
    assert client.get('/images/1').status_code == 200
