# Big Picture

## Project Overview

Big Picture is a web photo gallery. It currently supports these features:

1) Gallery view of uploaded images (http://apphost/images/).
2) Details view of any given uploaded image (http://apphost/images/detail/<id:int>)
3) Upload an individual image with title and description (http://apphost/images/add)
4) Upload an archive with any number of images (http://apphost/images/bulk)

Big Picture is built using Flask, SQLAlchemy, and Celery.

As currently configured, Big Picture uses Postgres (which provides good text search through tsquery). Celery is backed by a local Redis instance.

## Running the project

To run a local instance of the project on the Flask development server:

* Ensure there are a postgres and redis instance running on localhost
* Run `poetry install`.
* Start a celery worker. Example command from [this Miguel Grinberg blog](https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern).
	* `celery -A celery_worker.celery worker --loglevel=info`
* Export the env variable needed by Flask: `export FLASK_APP=big_picture`.
* Run the app: `poetry run flask run`.

## TODO

* Refactor upload filename access to consistently use app config values and Image filename helper
* Update application configuration to support both containerized and non-containerized builds.

## Configuration notes

For running regular instance:

* Currently expects a postgres instance on localhost with username, password, and database `big_picture`.

For running a test instance:

* Expects a postgres instance on localhost with username and password `big_picture` and database `big_picture_test`.

Color scheme link: [Color Scheme](https://coolors.co/16bac5-5fbff9-efe9f4-171d1c-5863f8)
