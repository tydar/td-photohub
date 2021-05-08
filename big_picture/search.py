from flask import render_template, Blueprint, request
from big_picture.models.image import Image
from sqlalchemy import or_
from functools import reduce

import os

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET', 'POST'])
def simple():
    if request.method == 'POST':
        search = request.form['search']

        # need to sanitize the input to replace whitespace with | or operators
        tokens = search.split()
        new_query = reduce(lambda s1, s2: s1 + '|' + s2, tokens)

        # get the list using the sqlachemy or_
        # this generates a potgres query using to_tsquery
        res_list = Image.query.filter(
            or_(
                Image.title.match(new_query),
                Image.description.match(new_query)
            )
        ).all()

        # create the static file path and pair it in a tuple with each Image object
        # then pass that list of tuples to the template for search results
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
