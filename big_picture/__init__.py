import os
from flask import Flask

def create_app(test_config=None):
    # create and configure Flask app per Flask project structure guidelines
    app = Flask(__name__, instance_relative_config=True)

    # later add DB config details here
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://big_picture:big_picture@localhost/big_picture',
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

    # simple route to test setup
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import images
    app.register_blueprint(images.bp)


    from . import search
    app.register_blueprint(search.bp)

    return app
