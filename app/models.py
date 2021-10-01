from app import db

# sqlalchemy provides a class called Model that is a declarative base which can be used to declare models:
class Contestant(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    country = db.Column(db.Text)
    season = db.Column(db.Integer)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(80))
    description = db.Column(db.String(500))
    is_eliminated = db.Column(db.Boolean)
    tribals = db.relationship('Tribal', backref=db.backref('contestant'))

    def __repr__(self):
        return f'{self.name}'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    #votes = db.relationship('Vote', backref=db.backref('user'))

    def __repr__(self):
            return f'{self.firstname}'

class Tribal(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tribal_date = db.Column(db.DateTime, primary_key=True, nullable=False)
    voted_out_id = db.Column(db.Integer, db.ForeignKey('contestant.id'), nullable=True)
 

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tribal_id = db.Column(db.Integer, db.ForeignKey('tribal.id'), nullable=False)
    first_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'), nullable=False)
    second_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
    third_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
    