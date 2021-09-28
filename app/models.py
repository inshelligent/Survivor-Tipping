from app import db

# sqlalchemy provides a class called Model that is a declarative base which can be used to declare models:
class Contestant(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(80))
    description = db.Column(db.Text)
    is_eliminated = db.Column(db.Boolean)

    def __repr__(self):
        return '<Contestant %r>' % self.name