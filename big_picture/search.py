from flask import render_template, Blueprint, request
from big_picture.models.image import Image
import os
from sqlalchemy import or_

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET', 'POST'])
def simple():
    if request.method == 'POST':
        search = request.form['search']
        res_list = Image.query.filter(
            or_(
                Image.title.match(search),
                Image.description.match(search)
            )
        ).all()
        path_list = []
        for res in res_list:
            filename = res.title + str(res.id) + '.' + res.ext
            path = os.path.join('upload/', filename)
            path_list.append((res, path))
        return render_template('search/results.html', path_list=path_list)
    return render_template('search/simple.html')

@bp.route('/advanced')
def advanced():
    return render_template('search/advanced.html')
