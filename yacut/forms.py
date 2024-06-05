from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Regexp

from .constants import MAX_LENGTH_OF_SHORT_URL, REGEXP


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, MAX_LENGTH_OF_SHORT_URL),
            Optional(),
            Regexp(
                REGEXP,
                message='Короткая ссылка может содержать только буквы и цифры'
            )
        ]
    )
    submit = SubmitField('Создать')
