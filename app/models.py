from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

# sqlalchemy provides a class called Model that is a declarative base which can be used to declare models:

# this holds all the details for a user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    votes = db.relationship('Vote', backref='user')

    def __repr__(self):
            return f'{self.firstname}'
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
# this holds all the details for a contestant
class Contestant(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    country = db.Column(db.Text)
    season = db.Column(db.Integer)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(80))
    description = db.Column(db.String(500))
    is_eliminated = db.Column(db.Boolean)

    def __repr__(self):
        return f'{self.name}'

# this holds all the details for a tribal/elimination, and needs contestant
class Tribal(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tribal_date = db.Column(db.DateTime, nullable=False)
    voted_out_id = db.Column(db.Integer, db.ForeignKey('contestant.id'), default=0)
 
# this holds all the details for a vote, and needs user, tribal, and contestant
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tribal_id = db.Column(db.Integer, db.ForeignKey('tribal.id'), nullable=False)
    first_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'), nullable=False)
    second_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
    third_choice_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
    first_choice = db.relationship('Contestant', foreign_keys=first_choice_id)
    second_choice = db.relationship('Contestant', foreign_keys=second_choice_id)
    third_choice = db.relationship('Contestant', foreign_keys=third_choice_id)
    #user = db.relationship('User', foreign_keys=user_id)
    tribal = db.relationship('Tribal', foreign_keys=tribal_id)
