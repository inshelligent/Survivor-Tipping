import csv
from datetime import date, datetime
from sqlalchemy import desc, null
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.sql.expression import null   # Flask is already imported in _init_

from app import app, db

from app.models import Contestant, User, Tribal, Vote
from app.forms import AddUserForm, LoginForm, AddVoteForm, AddContestantForm, EditContestantForm, EliminateContestantForm, AddTribalForm

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

def get_contestants_in_game():
    # A helper function that returns a list of tuples with contestant ids and names from the contestants table.
    # This is used to populate the choices in the Contestants for each voting choice dropdown.
    contestant_choices = []
    contestant_choices.insert(0, (0, ""))
    for contestant in Contestant.query.all():
        if contestant.is_eliminated==False:
            choice = (contestant.id, contestant.name)
            contestant_choices.append(choice)
    return contestant_choices
    #contestants = [(x.id, x.name) for x in Contestant.query.all() if x.is_eliminated==False]
    #return contestants

def get_current_contestants():
    # A helper function that returns a list of tuples with contestant ids and names from the contestants table.
    # This is used to populate the choices in the Contestants for each voting choice dropdown.
    contestants = [(player.id, player.name) for player in Contestant.query.filter_by(is_eliminated=False)]
    return contestants

def get_current_tribals():
    # A helper function that returns a list of tuples with tribal ids and dates from the tribals table.
    # This is used to populate the choices for the tribal choice dropdown, in the Vote form and on the Eliminate Contestant admin page
    # thanks to stackoverflow for how to format the date :)
    tribals = [(tribal.id, tribal.tribal_date.strftime("%a %d %b %Y")) for tribal in Tribal.query.filter_by(voted_out_id=0)]
    return tribals


# HOMEPAGE
@app.route('/')
@app.route('/index')
def index():
    user = ""   # need to add some logic to check for logged in user
    comments = load_from_file('chat.csv')  # TO-DO IF TIME
    return render_template('index.html', title=TITLE, user=user, comments=comments)

@app.route('/admin')
def admin():
    user = ""   # need to add some logic to check for logged in user
    return render_template('admin.html', title=TITLE, user=user)

# CONTESTANTS SECTION #
# Public Contestants page which lists all the players/competitors in the show, separated by eliminated status
@app.route('/contestants')
def contestants():
    #players = load_from_file('competitors.csv')  # convert this to fetch from DB instead
    # The records from the table are retrieved and put in an Iterable data structure (essentially a list)
    contestants = Contestant.query.all()
    # Returns the view with list of contestants
    return render_template('contestants.html', players=contestants, title="Meet the contestants")

@app.route('/admin_contestants')
def admin_contestants():
    # The records from the table are retrieved and put in an iterable data structure
    contestants = Contestant.query.all()
    # Returns the view with list of contestants
    return render_template('admin_contestants.html', contestants=contestants, title="Contestant Admin")

@app.route('/add_contestant', methods=['GET', 'POST'])
def add_contestant():
    form = AddContestantForm()
    # Check if the form has been submitted (is a POST request) and form inputs are valid
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Create a Contestant object for saving to the database, mapping form inputs to object
        contestant = Contestant()
        form.populate_obj(obj=contestant)
        # Adds the contestant object to session for creation and saves changes to db
        db.session.add(contestant)
        db.session.commit()
        flash('Contestant was added successfully!')
        # Returns the view with a message that the contestant has been added
        # return render_template('add_contestant.html', contestant = contestant, title="Contestant Added")
        return redirect(url_for('admin_contestants'))
    # When there is a GET request, the view with the form is returned
    return render_template('add_contestant.html', form = form)

@app.route('/edit_contestant/<int:id>', methods = ['GET', 'POST'])
def edit_contestant(id):
    # Retrieves the contestant record for the given id, if it exists
    contestant = Contestant.query.get_or_404(id)

    # Creates a form for editing the contestant record, putting in the contestant record's details
    form = EditContestantForm(obj=contestant)
    #form.name.choices = get_current_contestants()

    # Check if the form has been submitted (is a POST request) and form inputs are valid
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Create a Contestant object for saving to the database, mapping form inputs to object
        form.populate_obj(contestant)
        # Adds the contestant object to session for creation and saves changes to db
        db.session.commit()
        flash('Contestant details were saved successfully!')

        # Returns the view with a message that the contestant has been added
        return redirect(url_for('admin_contestants'))

    # When there is a GET request, the view with the form is returned
    contestant_name = f'{contestant.name}'
    return render_template('edit_contestant.html', form = form, contestant_name = contestant_name)

@app.route('/delete_contestant/<int:id>')
def delete_contestant(id):
    # Retrieves the contestant record for the given id
    contestant = Contestant.query.get_or_404(id)
    # The fruit record is deleted
    db.session.delete(contestant)
    # The change (the deletion) are saved in the database file
    db.session.commit()
    flash('Contestant was deleted successfully!')

    # Returns the view that displays the list of fruits
    return redirect(url_for('admin_contestants'))

@app.route('/eliminate_contestant', methods=['GET', 'POST'])
def eliminate_contestant():
    form = EliminateContestantForm()
    # gets the choices for the current Tribals
    form.tribal_id.choices = get_current_tribals()
    # gets the choices for the contestants form field
    form.voted_out_id.choices = get_current_contestants()
    # Check if the form has been submitted (is a POST request) and form inputs are valid
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        tribalTemp = Tribal()
        form.populate_obj(obj=tribalTemp)
        # get the existing contestant info
        contestant = Contestant.query.get_or_404(tribalTemp.voted_out_id)
        # update the is_eliminated field
        contestant.is_eliminated = True
        # get the existing tribal info
        tribal = Tribal.query.get_or_404(tribalTemp.tribal_id)
        # update the voted_out_id field with the selected contestant's id
        tribal.voted_out_id = tribalTemp.voted_out_id

        ''' UPADATING USER SCORES
            Update the score of all users based on who was voted out
            10 points if voted out is 1st choice
            3 points if voted out is 2nd choice
            1 point if voted out is 3rd choice
        '''
        # store the id of the eliminated contestant
        voted_out = contestant.id
        # get the votes for tonight's tribal and update the user scores
        for vote in Vote.query.filter_by(tribal_id=tribalTemp.tribal_id):
            user = vote.user
            if vote.first_choice_id == contestant.id:
                user.score += 10
            elif vote.second_choice_id == contestant.id:
                user.score += 3
            elif vote.third_choice_id == contestant.id:
                user.score += 1
        
        # save all the changes to the DB
        db.session.commit()

        return redirect(url_for('admin_contestants'))

    return render_template('eliminate_contestant.html', form = form)

# TRIBAL SECTION #
# Admin Tribal Page - allows an admin to create a tribal record
@app.route('/add_tribal', methods = ['GET', 'POST'])
def add_tribal():
    form = AddTribalForm()
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Get data from the form and put in a Vote object
        tribal = Tribal()
        form.populate_obj(obj=tribal)
        # Adds the tribal object to session for creation and saves changes to db
        db.session.add(tribal)
        db.session.commit()
        
        # Returns the view with a message that the student has been added
        return redirect(url_for('admin'))
    # Returns the view with a message of how to bet, and list of remaining contestants
    return render_template('add_tribal.html', form = form, title="Create a Tribal")


# VOTING SECTION #
# Send user to the Tipping page - allows user to place a tip, then saves to the votes table
@app.route('/vote', methods = ['GET', 'POST'])
def vote():
    form = AddVoteForm()
    # store the user_id in a hidden field on the form
    #form.user_id = 2          # This did not work ### HARD CODED USER ID FOR NOW
    # gets the choices for the current Tribals
    form.tribal_id.choices = get_current_tribals()
    # gets the choices for the contestants form field
    form.first_choice_id.choices = get_contestants_in_game()
    form.second_choice_id.choices = get_contestants_in_game()
    form.third_choice_id.choices = get_contestants_in_game()
    # Check if the form has been submitted (is a POST request) and form inputs are valid
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Get data from the form and put in a Vote object
        vote = Vote()
        form.populate_obj(obj=vote)
        vote.user_id = 2          # !!! HARD CODED USER ID FOR NOW !!!
        # Adds the vote object to session for creation and saves changes to db
        db.session.add(vote)
        db.session.commit()
        
        # Returns the view with a message that the student has been added
        #return redirect(url_for('vote_successful'))
        return render_template('vote_successful.html', vote = vote, title="Vote Placed")
    
    # Returns the view with a message of how to bet, and list of remaining contestants
    return render_template('vote.html', form = form, title="Voting")

# USER SECTION #
# Send user to Sign-up / registration page
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = AddUserForm()
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Create a Contestant object for saving to the database, mapping form inputs to object
        user = User()
        form.populate_obj(obj=user)
        # Adds the user object to session for creation and saves changes to db
        db.session.add(user)
        db.session.commit()
        ####### DISPLAY SOME KIND OF SUCCESS MESSAGE #### "Sign Up Successful"
        # Take user back to home page
        return redirect(url_for('index'))

    return render_template('sign_up.html', form = form, title="Sign Up")

# send user to the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Create a user object for checking stuff, mapping form inputs to object
        tempUser = User()
        form.populate_obj(obj=tempUser)
        # find out if they are a registered user
        #user = User.query.get_or_404(tempUser.username)
        # if they are, display welcome message and save their ID and is_admin status
        ######## DO STUFF HERE ########
        # Take user back to home page
        return redirect(url_for('index'))

    return render_template('login.html', form = form, title="Log In")

###### TO-DO ####### Do we need this??
# Sign-up / registration form submit   
"""@app.route('/signup-received', methods = ["POST"])
def submit_sign_up():
    new_user = {}
    if request.method == "POST":
        new_user['name'] = request.form.get('name')
        new_user['username'] = request.form.get('username')
        new_user['pword'] = request.form.get('pword')
        new_user['email'] = request.form.get('email')
        new_user['score'] = 0
        # Returns the view with a message that the user has been added
        return render_template('sign_up_received.html', new_user = new_user, title="Sign Up Successful") """

###### TO-DO ####### Do we need this??
# login page form submit
"""@app.route('/login-received', methods = ["POST"])
def check_login():
    if request.method == "POST":
        user_name = request.form.get('username')
        pword = request.form.get('pword')
        # Add verfication and if statement depending on results, dummy code assumes 
        comments = load_from_file('chat.csv')
        user = {'username': user_name}
        # Returns the view with a message that the user is now logged in
        return render_template('index.html', title=TITLE, user=user, comments=comments) """

# Leaderboard page which lists all the players/app users, ordered by score desc
@app.route('/leaderboard')
def leaderboard():
    #fetch users from DB
    # The records from the table are retrieved and put in an Iterable data structure (essentially a list)
    user = user = User.query.order_by(User.score.desc())
    # Returns the view with list of users ordered from highest scoring to lowest
    return render_template('leaderboard.html', players=user, title="Australian Survivor 6 - Leaderboard")

