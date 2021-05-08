from flask import render_template, Blueprint

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET', 'POST'])
def gallery():
    return render_template('search/simple.html')

@bp.route('/advanced')
def add_image():
    return render_template('search/advanced.html')
