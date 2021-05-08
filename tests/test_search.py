import pytest
from big_picture.models.image import Image

def test_simple(client, app):
    rv = client.get('/search/')
    assert rv.status_code == 200
    assert b'Search' in rv.data

    search = 'TEST_1'
    rv_post = client.post(
        '/search/',
        data = {'search': search},
    )

    assert b'TEST_1' in rv_post.data


def test_advanced(client, app):
    assert client.get('/search/advanced').status_code == 200
