from flask import render_template, Blueprint, flash, request, redirect, url_for, current_app
import os
from werkzeug.utils import secure_filename
from big_picture.models import db
from big_picture.models.image import Image


bp = Blueprint('images', __name__, url_prefix='/images')


### UTIL

# TODO: move to its own section
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

### CONTROLLERS

@bp.route('/')
def gallery():
    return render_template('images/gallery.html')

@bp.route('/<int:image_id>')
def image_details(image_id):
    # Pull image by ID
    return render_template('images/details.html')

@bp.route('/add', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        # check for file attached
        if 'file' not in request.files:
            flash('File not attached')
            return redirect(request.url)
        upload = request.files['file']
        # check that file selected
        if upload.filename == '':
            flash('No file selected')
            return redirect(request.url)
        # check that file has an image extension
        # create record in DB for file to generate unique file name
        # save file
        if upload and allowed_file(upload.filename):
            title = secure_filename(request.form['title'])
            extension = upload.filename.rsplit('.', 1)[1].lower()
            db_rec = Image(title=title)
            db.session.add(db_rec)
            db.session.commit()
            # db_rec has ID because change has been committed
            filename = title + str(db_rec.id) + '.' + extension
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            print(path)
            upload.save(path)
            flash('File uploaded successfully.')
            return redirect(url_for('image_details', image_id=db_rec.id))
    return render_template('images/add.html')
