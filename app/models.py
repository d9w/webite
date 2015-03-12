from .app import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def config(self):
        return dict(id = self.id,
                name = self.name)
