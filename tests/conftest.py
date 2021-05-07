import pytest
from big_picture import create_app
from big_picture.models import db
from datetime import datetime

@pytest.fixture
def app():
    # set up DB here later
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql+psycopg2://big_picture:big_picture@localhost/big_picture_test',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'UPLOAD_FOLDER': 'tests/static/upload/',
    })

    from big_picture.models.image import Image
    test1 = Image(title='TEST_1', description='TEST_DESC_1')

    with app.app_context():
        db.create_all()
        db.session.add(test1)
        db.session.commit()

        yield app

        db.session.close()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
