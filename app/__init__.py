from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survivor.db'

db = SQLAlchemy(app)

from app import routes, models

@app.cli.command('create-db')
def create_db():

    # Create the database for the app from scratch
    db.drop_all()
    db.create_all()

    # Create a contestant record for Hayley
    #hayley = models.Contestant(id=1, name='Hayley', age=31, occupation='Pain Researcher', description='Master charmer and academic researcher Hayley is a switched-on Australian Survivor superfan who plans to excel in the game of competitive manipulation. As a professional Pain Researcher, her job is to administer placebo psychological therapy to patients and test the brains response to treatment. Also wielding a degree in physiotherapy, Hayley plans to make friends with her healing hands.')
    hayley = models.Contestant(id=1, name='Hayley', age=31, occupation='Pain Researcher', description='test')
    db.session.add(hayley)

    # Create a contestant record for George
    #george = models.Contestant(id=2, name='George', age=31, occupation='Public Servant', description='A self-described â€˜spin-doctor for the governmentâ€™, Bankstown Labor Party President George believes his whole career has been preparing him for the game of Australian Survivor. Cunning, an expert negotiator and a master manipulator, this high achiever will stop at nothing to make it to the final Tribal Council.')
    george = models.Contestant(id=2, name='George', age=31, occupation='Public Servant', description='test')
    db.session.add(george)

    # Save the created records to the database file
    db.session.commit()

