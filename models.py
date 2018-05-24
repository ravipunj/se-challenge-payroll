import datetime

from app import db

class TimeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False, default=lambda: None)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return "[TimeReport id={id}]".format(id=self.id)