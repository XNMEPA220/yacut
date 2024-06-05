import random
import string

from flask import render_template, abort, redirect, flash

from .models import URLMap
from .forms import URLForm
from . import app, db


def get_unique_short_id():
    short_id = ''.join(random.choices(string.hexdigits, k=6))
    if URLMap.query.filter_by(short=short_id).first() is not None:
        return get_unique_short_id()
    return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        short_id = form.custom_id.data
        if URLMap.query.filter_by(short=short_id).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('yacut.html', form=form)
        if not short_id:
            short_id = get_unique_short_id()
        url_map = URLMap(original=original_link, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return render_template('yacut.html', short_id=short_id, form=form)
    return render_template('yacut.html', form=form)


@app.route('/<short_id>')
def redirect_to_full_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        abort(404)
    original_link = url_map.original
    return redirect(original_link)
