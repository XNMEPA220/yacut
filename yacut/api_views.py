from re import fullmatch

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id
from .constants import REGEXP


@app.route('/api/id/', methods=['POST'])
def create_id():
    try:
        data = request.get_json()
    except:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    short_id = data.get('custom_id')
    if not short_id:
        short_id = get_unique_short_id()
    if len(short_id) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if not fullmatch(REGEXP, short_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if (
            URLMap.query.filter_by(short=short_id).first() is not None
    ):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    url_map = URLMap(original=data['url'], short=short_id)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    original_link = url_map.original
    return jsonify({'url': original_link}), 200
