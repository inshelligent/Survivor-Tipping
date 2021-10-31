import os

from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
# Sets up configuration setting for the database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survivor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turns this setting off, helps with performance
# allow us to see the SQL commands that are being run and any errors/messages to help with debugging
app.config['SQLALCHEMY_ECHO'] = True
# stops cross-script forgery, used with WTForms
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Set up the login manager for the app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

from app import models, forms, routes

@app.cli.command('create-db')
def create_db():

    # Create the database for the app from scratch
    db.drop_all()
    db.create_all()

    # Create a contestant record for Hayley
    # description might be a bit long (92 characters truncated)
    hayley = models.Contestant(season = 6,
                                country = 'Australia',
                                name='Hayley', 
                                age=31, 
                                occupation='Pain Researcher', 
                                description='Master charmer and academic researcher Hayley is a switched-on Australian Survivor superfan who plans to excel in the game of competitive manipulation. As a professional Pain Researcher, her job is to administer placebo psychological therapy to patients and test the brains response to treatment. Also wielding a degree in physiotherapy, Hayley plans to make friends with her healing hands.', 
                                is_eliminated=False)
    db.session.add(hayley)

    # Create a contestant record for George
    # description might be a bit long (13 characters truncated)
    george = models.Contestant(season = 6,
                        country = 'Australia',
                        name='George', 
                        age=31, 
                        occupation='Public Servant', 
                        description="A self-described 'spin-doctor for the government', Bankstown Labor Party President George believes his whole career has been preparing him for the game of Australian Survivor. Cunning, an expert negotiator and a master manipulator, this high achiever will stop at nothing to make it to the final Tribal Council.", 
                        is_eliminated=False)
    db.session.add(george)

    # Create a contestant record for Wai
    wai = models.Contestant(season = 6,
                        country = 'Australia',
                        name='Wai', 
                        age=38, 
                        occupation='Author', 
                        description='As an international award-winning Author of six children and young adult books, Wai is an academic powerhouse. With degrees from some of the most prestigious Universities in the world, this self-proclaimed nerd is a book worm with passionate purists.', 
                        is_eliminated=False)
    db.session.add(wai)

    # Create a contestant record for Flick
    flick = models.Contestant(season = 6,
                        country = 'Australia',
                        name='Flick', 
                        age=28, 
                        occupation='Big Wave Surfer', 
                        description="Currently ranked second in the world for Big Wave Surfing, it's no surprise that Flick is a fearless and strong competitor. She holds the record for the biggest wave surfed by an Australian woman and is also an accomplished artist, with exhibitions in the works.", 
                        is_eliminated=False)
    db.session.add(flick)

    # Create a contestant record for Cara
    # description might be a bit long (46 characters truncated)
    cara = models.Contestant(season = 6,
                        country = 'Australia',
                        name='Cara', 
                        age=47, 
                        occupation='Real Estate Agent', 
                        description="Real Estate Agency Owner Cara, may be known as the Duchess of Double Bay, but can she bring her reign to the Outback? At the age of 20, the quirky adventure seeker realised that she had a secret power. As an empath, Cara can sense and feel emotions as if they're part of her own experience and someone else's pain and happiness, become her own.", 
                        is_eliminated=True)
    db.session.add(cara)
    db.session.commit()

    admin = models.User(username = "admin",
                        password_hash = os.environ.get('ADMIN_PASSWORD'),
                        email = "admin@blah.com.au",
                        firstname = "Admin",
                        surname = "User",
                        is_admin = True,
                        score = 0)
    db.session.add(admin)

    general = models.User(username = "joebloggs",
                        password_hash = os.environ.get('JOE_PASSWORD'),
                        email = "joe@blah.com.au",
                        firstname = "Joe",
                        surname = "Bloggs",
                        is_admin = False,
                        score = 0)
    db.session.add(general)
    # Save the created records to the database file
    db.session.commit()

    # create some test data for Tribals
    round1 = models.Tribal(tribal_date = date.today())
    db.session.add(round1)
    # Save the created records to the database file
    db.session.commit()

