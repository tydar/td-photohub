import pytest
from big_picture.models import db
from big_picture.models.image import Image

## Test models

def test_image_model(client, app):
    with app.app_context():
        assert len(Image.query.filter_by(title='TEST_1').all()) == 1

## Test views

def test_hello(client, app):
    assert client.get('/hello').status_code == 200

def test_gallery(client, app):
    assert client.get('/images/').status_code == 200

def test_add(client, app):
    assert client.get('/images/add').status_code == 200

def test_details(client, app):
    assert client.get('/images/1').status_code == 200
