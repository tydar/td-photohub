import pytest
from big_picture import create_app
from big_picture.models import db
from datetime import datetime
from big_picture import celery

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql+psycopg2://big_picture:big_picture@localhost/big_picture_test',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'UPLOAD_FOLDER': 'tests/static/upload/',
    })

    from big_picture.models.image import Image
    test1 = Image(title='TEST_1', description='TEST_DESC_1', ext='jpg')
    comp_desc = 'This is a more complex description. Pretend the picture is a big fish.'
    test_complex_desc = Image(title='TEST_2', description=comp_desc, ext='jpg')

    with app.app_context():
        db.create_all()
        db.session.add(test1)
        db.session.add(test_complex_desc)
        db.session.commit()

        yield app

        db.session.close()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://localhost:6379/0',
        'result_backend': 'redis://localhost:6379/0'
    }

@pytest.fixture(scope='module')
def celery_app(request):
    return celery
