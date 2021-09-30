from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Sets up configuration setting for the database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survivor.db'
# allow us to see the SQL commands that are being run and any errors/messages to help with debugging
app.config['SQLALCHEMY_ECHO'] = True
# stops cross-script forgery, used with WTForms
app.config['SECRET_KEY'] = 'Survive-is-the-key'

db = SQLAlchemy(app)

from app import models, forms, routes

@app.cli.command('create-db')
def create_db():

    # Create the database for the app from scratch
    db.drop_all()
    db.create_all()

    # Create a contestant record for Hayley
    # description might be a bit long (92 characters truncated)
    hayley = models.Contestant(id=1, 
                                name='Hayley', 
                                age=31, 
                                occupation='Pain Researcher', 
                                description='Master charmer and academic researcher Hayley is a switched-on Australian Survivor superfan who plans to excel in the game of competitive manipulation. As a professional Pain Researcher, her job is to administer placebo psychological therapy to patients and test the brains response to treatment. Also wielding a degree in physiotherapy, Hayley plans to make friends with her healing hands.', 
                                is_eliminated=False)
    db.session.add(hayley)

    # Create a contestant record for George
    # description might be a bit long (13 characters truncated)
    george = models.Contestant(id=2, 
                        name='George', 
                        age=31, 
                        occupation='Public Servant', 
                        description="A self-described 'spin-doctor for the government', Bankstown Labor Party President George believes his whole career has been preparing him for the game of Australian Survivor. Cunning, an expert negotiator and a master manipulator, this high achiever will stop at nothing to make it to the final Tribal Council.", 
                        is_eliminated=False)
    db.session.add(george)

    # Create a contestant record for Wai
    wai = models.Contestant(id=3, 
                        name='Wai', 
                        age=38, 
                        occupation='Author', 
                        description='As an international award-winning Author of six children and young adult books, Wai is an academic powerhouse. With degrees from some of the most prestigious Universities in the world, this self-proclaimed nerd is a book worm with passionate purists.', 
                        is_eliminated=False)
    db.session.add(wai)

    # Create a contestant record for Flick
    flick = models.Contestant(id=4, 
                        name='Flick', 
                        age=28, 
                        occupation='Big Wave Surfer', 
                        description="Currently ranked second in the world for Big Wave Surfing, it's no surprise that Flick is a fearless and strong competitor. She holds the record for the biggest wave surfed by an Australian woman and is also an accomplished artist, with exhibitions in the works.", 
                        is_eliminated=False)
    db.session.add(flick)

    # Create a contestant record for Cara
    # description might be a bit long (46 characters truncated)
    cara = models.Contestant(id=5, 
                        name='Cara', 
                        age=47, 
                        occupation='Real Estate Agent', 
                        description="Real Estate Agency Owner Cara, may be known as the Duchess of Double Bay, but can she bring her reign to the Outback? At the age of 20, the quirky adventure seeker realised that she had a secret power. As an empath, Cara can sense and feel emotions as if they're part of her own experience and someone else's pain and happiness, become her own.", 
                        is_eliminated=True)
    db.session.add(cara)

    # Save the created records to the database file
    db.session.commit()
