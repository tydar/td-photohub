import pytest
from big_picture.models import db
from big_picture.models.image import Image

## Test models

def test_image_model(client, app):
    with app.app_context():
        assert len(Image.query.filter_by(title='TEST_1').all()) == 1

## Test views

def test_gallery(client, app):
    # wishlist: test pagination
    rv = client.get('/images/1')
    assert rv.status_code == 200
    assert b'TEST_1' in rv.data
    assert b'TEST_2' in rv.data

def test_add(client, app):
    rv = client.get('/images/add')
    assert rv.status_code == 200
    assert b'Upload' in rv.data

    # must use 'rb' for mode to open as byte stream
    # for upload to work as POST data
    with open('tests/test_img.png', 'rb') as upload:
        title = 'AUTO_TEST_TITLE'
        desc = 'AUTO_TEST_DESC'
        post_rv = client.post(
            '/images/add',
            data={'title': title, 'desc': desc, 'file': upload},
        )

    assert len(Image.query.filter_by(title='AUTO_TEST_TITLE').all()) == 1

def test_details(client, app):
    rv = client.get('/images/detail/1')
    assert rv.status_code == 200
    assert b'TEST_1' in rv.data


def test_zip_upload(client, app):
    rv = client.get('/images/bulk')
    assert rv.status_code == 200
    assert b'Upload' in rv.data


    # post test designed to upload a zip file containing 3 images
    with open('tests/test_zip.zip', rb) as upload:
        post_rv = client.post(
            '/images/bulk',
            data={'prefix': prefix, 'file': upload},
        )
    assert len(Image.query.filter_by(Image.title.match('PRE_')).all()) == 3
