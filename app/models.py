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

    def __repr__(self):
        return f'{self.name}'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    user_level = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.id} {self.username} {self.firstname}'


class Tribal(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tribal_date = db.Column(db.DateTime, primary_key=True, nullable=False)
    voted_out_id = db.Column(db.Integer, db.ForeignKey('contestant.id'), nullable=False)
    
    def __repr__(self):
        return f'{self.tribal_id} {self.voted_out_id}'

class Vote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    tribal_id = db.Column(db.Integer, db.ForeignKey('tribal.id'), primary_key=True, nullable=False)
    first_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'), nullable=False)
    second_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
    third_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
    
    def __repr__(self):
        return f'{self.user_id} {self.tribal_id} {self.first_choice_id}'