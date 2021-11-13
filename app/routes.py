import csv
#from datetime import date, datetime
#from sqlalchemy import desc, null
from flask import render_template, flash
#from sqlalchemy.sql.expression import null   # Flask is already imported in _init_
from flask_login import current_user, login_required

from app import app, db

from app.models import Contestant, User, Tribal, Vote
from app.forms import AddVoteForm


TITLE = "Cosy Couch Survivor"

# multi-purpose function that reads a file into a list then returns a list object
# is used by homepage so it needs to be up here first
def load_from_file(fname):
    # loads the contents from a given csv file
    contents = []
    with open(fname) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            contents.append(row)
    return contents

def get_current_contestants():
    ''' A helper function that returns a list of tuples with
    contestant ids and names from the contestants table
    if they have not been eliminated. Used to populate the 
    vote choices for each voting choice dropdown. '''
    contestants = [(player.id, player.name) for player in Contestant.query.filter_by(is_eliminated=False)]
    contestants.insert(0, (0, "Select who's going home"))
    return contestants

def get_current_tribals():
    ''' A helper function that returns a list of tuples with 
    tribal ids and dates from the tribals table.
    Used to populate the choices for the tribal choice dropdown
    in the Vote form and on the Eliminate Contestant admin page '''
    tribals = [(tribal.id, tribal.tribal_date.strftime("%a %d %b %Y")) for tribal in Tribal.query.filter_by(voted_out_id=0)]
    return tribals


# HOMEPAGE
@app.route('/')
@app.route('/index')
def index():
    comments = load_from_file('chat.csv')  # TO-DO IF TIME
    return render_template('index.html', title=TITLE, comments=comments)


# CONTESTANTS SECTION #
# Public Contestants page which lists all the players/competitors in the show, separated by eliminated status
@app.route('/contestants')
#@login_required
def contestants():
    # Get records from the table and send to View to display contestants
    contestants = Contestant.query.all()
    return render_template('contestants.html', players=contestants, title="Meet the contestants")


# VOTING SECTION #
# Send user to the Tipping page - allows user to place a tip, then save to db
@app.route('/vote', methods = ['GET', 'POST'])
@login_required
def vote():
    form = AddVoteForm()
    # populate dropdowns
    form.tribal_id.choices = get_current_tribals()
    form.first_choice_id.choices = get_current_contestants()
    form.second_choice_id.choices = get_current_contestants()
    form.third_choice_id.choices = get_current_contestants()
    # Check if the form has been submitted (is a POST request) and form inputs are valid
    if form.validate_on_submit():
        # Get data from the form and put in a Vote object
        vote = Vote()
        form.populate_obj(obj=vote)
        vote.user_id = current_user.id
        # check if this user has already voted for this Tribal before
        checkvote = Vote.query.filter_by(user_id=current_user.id,tribal_id=vote.tribal_id).first()
        if checkvote is None:
            # Adds the vote object to session for creation and saves changes to db
            db.session.add(vote)
            db.session.commit()
            # Returns the view with a message that the vote has been added
            return render_template('vote_successful.html', vote = vote, title="Vote Placed")

        # Already voted, leave the user on this screen with message
        flash('You have already voted in this Tribal!')
    
    # Returns the view with a message of how to bet, and list of remaining contestants
    return render_template('vote.html', form = form, title="Voting")


# Leaderboard page which lists all the users, ordered by score desc
@app.route('/leaderboard')
@login_required
def leaderboard():
    # Retrieved users from the db and order by score highest to lowest
    #user = user = User.query.order_by(User.score.desc())
    user = User.query.order_by(User.score.desc())

    return render_template('leaderboard.html', players=user, title="Australian Survivor 6 - Leaderboard")

