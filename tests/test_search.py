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

def test_simple_complex_desc(client, app):
    """
    Tests both a multi-token search and a search with whitespace.

    Postgres as a backend => to_tsquery requires searches to exclude whitespace
    """

    search = 'pretend THE'
    rv_post = client.post(
        '/search/',
        data = {'search': search}
    )

    assert b'TEST_2' in rv_post.data

def test_advanced(client, app):
    assert client.get('/search/advanced').status_code == 200
