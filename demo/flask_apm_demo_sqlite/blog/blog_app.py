from flask import Blueprint, render_template, current_app

from db import db
from db.models import Page

app = Blueprint('blog', __name__, template_folder='templates')


@app.route('/')
@app.route('/index.html')
def index():
    current_app.logger.warn('View index')
    pages = db.paginate(db.select(Page), per_page=5)
    return render_template(
        'blog/index.jinja2',
        pages=pages
    )
