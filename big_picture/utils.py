import click
from flask import Blueprint
from big_picture.models import db

bp = Blueprint('utils', __name__)

@bp.cli.command('create-db')
def create_db():
    db.create_all()
