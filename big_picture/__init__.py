import os
from flask import Flask
from celery import Celery

celery = Celery(__name__, broker='redis://localhost:6379/0')
# TODO: create a separate configuration file so broker isn't hardcoded here
# Note also that this configuration means that the testing instance of redis will also
# be this instance, since this occurs prior to the test_config being loaded below
# Discussion at https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern

def create_app(test_config=None):
    # create and configure Flask app per Flask project structure guidelines
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://big_picture:big_picture@localhost/big_picture',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER='big_picture/static/upload/',
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    )

    if test_config is None:
        # load specified config for instance when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from big_picture.models import db
    db.init_app(app)

    # Init celery
    celery.conf.update(app.config)

    # simple route to test setup
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import images
    app.register_blueprint(images.bp)


    from . import search
    app.register_blueprint(search.bp)

    from . import utils
    app.register_blueprint(utils.bp)

    return app
