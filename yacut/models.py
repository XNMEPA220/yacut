from datetime import datetime

from flask import url_for

from . import db
from .constants import MAX_LENGTH_OF_SHORT_URL


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(MAX_LENGTH_OF_SHORT_URL), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for("redirect_to_full_url", short_id=self.short, _external=True)
        )
