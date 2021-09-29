from app import db

# sqlalchemy provides a class called Model that is a declarative base which can be used to declare models:
class Contestant(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(80))
    description = db.Column(db.String(500))
    is_eliminated = db.Column(db.Boolean)
    tribals = db.relationship('Tribal', backref=db.backref('contestant', lazy=False))
    votes = db.relationship('Vote', backref=db.backref('contestant', lazy=False))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    user_level = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, default=0)
    votes = db.relationship('Vote', backref=db.backref('user', lazy=False))

class Tribal(db.Model):
    tribal_date = db.Column(db.DateTime, primary_key=True, nullable=False)
    voted_out_id = db.Column(db.Integer, db.ForeignKey('contestant.id'), nullable=False)

class Vote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    tribal_date = db.Column(db.DateTime, db.ForeignKey('tribal.tribal_date'), primary_key=True, nullable=False)
    first_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'), nullable=False)
    second_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
    third_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
