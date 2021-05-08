from flask import render_template, Blueprint

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        search = request.form['search']
        res_list = Image.query.filter(
            Image.title.match(search),
            Image.description.match(search)
        ).all()
        return render_template('search/results.html', res_list=res_list)
    return render_template('search/simple.html')

@bp.route('/advanced')
def add_image():
    return render_template('search/advanced.html')
