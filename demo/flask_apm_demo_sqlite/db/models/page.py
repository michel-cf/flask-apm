from db import db


class Page(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    text = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Page %r>' % self.title
