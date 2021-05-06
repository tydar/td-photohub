from flask import render_template, Blueprint

bp = Blueprint('images', __name__, url_prefix='/images')

@bp.route('/')
def gallery():
    return render_template('images/gallery.html')

@bp.route('/<int:image_id>')
def image_details(image_id):
    # Pull image by ID
    return render_template('images/details.html')

@bp.route('/add')
def add_image():
    return render_template('images/add.html')
