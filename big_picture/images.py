from flask import render_template, Blueprint, flash, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from big_picture.models import db
from big_picture.models.image import Image
from . import celery
from celery.result import AsyncResult

import os
import uuid
from zipfile import ZipFile

bp = Blueprint('images', __name__, url_prefix='/images')


### UTIL

# TODO: move to its own section
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def zip_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() == 'zip'

### CELERY TASKS
@celery.task()
def process_zip_file(filename, task_name, prefix):
    # 1) Open ZIP file
    # 2) Iterate over images
    # 2a) Validate image extensions
    # 2b) Store metadata in postgres
    # 2c) Store image file in UPLOAD folder
    # 3) complete task
    # Possible issues in its current state:
    # - Not tracking failed uploads
    # - Not providing a report of what success means
    with ZipFile(filename) as zf:
        fn_list = zf.namelist()
        for fn in fn_list:
            if allowed_file(fn):
                # We add the prefix to the title now to maintain
                # the way that filenames are generated from Image records elsewhere
                split_fn = fn.rsplit('.', 1)
                title = secure_filename(prefix + split_fn[0])
                extension = split_fn[1]
                db_rec = Image(title=title, ext=extension)

                db.session.add(db_rec)
                db.session.commit()

                filename = title + str(db_rec.id) + '.' + extension
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                with zf.open(fn) as file_obj:
                    with open(path, 'wb') as write_to:
                        write_to.write(file_obj.read())


### CONTROLLERS

@bp.route('/')
def gallery_front():
    return redirect(url_for('images.gallery', page=1))

@bp.route('/<int:page>')
def gallery(page=1):
    images = Image.query.order_by(Image.upload_date.desc()).paginate(page=page, per_page=10)
    return render_template('images/gallery.html', images=images)

@bp.route('/detail/<int:image_id>')
def image_details(image_id):
    # Pull image by ID
    image = Image.query.get_or_404(image_id)

    filename = image.title + str(image.id) + '.' + image.ext
    path = os.path.join('upload/', filename)
    path = url_for('static', filename=path)

    return render_template('images/details.html', image=image, path=path)

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
            desc = request.form['desc']

            db_rec = Image(title=title, description=desc, ext=extension)

            db.session.add(db_rec)
            db.session.commit()

            # db_rec has ID because change has been committed
            filename = title + str(db_rec.id) + '.' + extension
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            print(path)
            upload.save(path)

            flash('File uploaded successfully.')
            return redirect(url_for('images.image_details', image_id=db_rec.id))
    return render_template('images/add.html')

@bp.route('/bulk', methods=['GET', 'POST'])
def add_bulk():
    # This controller will send the zip file to a Celery task
    # Celery task will unzip the file, save the metadata to the DB, and store files appropriately
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
        # 1) save file with unique filename
        # 2) send unique filename, prefix, and original filename to celery task
        if upload and zip_file(upload.filename):
            unique_fn = uuid.uuid4().hex + '.zip'
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_fn)
            upload.save(path)
            task_instance = process_zip_file.delay(path, upload.filename, request.form['prefix'])
            return redirect(url_for('images.task', task_id=task_instance.id))
    return render_template('images/bulk.html')

@bp.route('/task/<task_id>')
def task(task_id):
    task = process_zip_file.AsyncResult(task_id)
    print(task.state)
    ready = False
    if task.state == 'SUCCESS':
        ready = True
    return render_template('images/tasks.html', status=ready)
