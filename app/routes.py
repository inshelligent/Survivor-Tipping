import csv
from datetime import date

from flask import render_template, request, redirect, url_for  # Flask is already imported in _init_

from app import app, db

from app.models import Contestant, User, Tribal, Vote
from app.forms import AddVoteForm, AddContestant, EditContestant

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
    ''' A helper function that returns a list of
        tuples with contestant ids and names from the contestants table.
        This is used to populate the choices in the Contestants for each voting choice dropdown.
    '''
    contestants = [(player.id, player.name) for player in Contestant.query.filter_by(is_eliminated=False)]
    return contestants
# HOMEPAGE
@app.route('/')
@app.route('/index')
def index():
#    user = {'username': 'Kylie'}   need to add some logic to check for logged in user
    user = ""
    comments = load_from_file('chat.csv')
    return render_template('index.html', title=TITLE, user=user, comments=comments)

# Send user to Contestants page which lists all the players/competitors in the show
@app.route('/contestants')
def contestants():
    #players = load_from_file('competitors.csv')  # convert this to fetch from DB instead
    # The records from the table are retrieved and put in an Iterable data structure (essentially a list)
    contestants = Contestant.query.all()
    # Returns the view with list of contestants
    return render_template('contestants.html', players=contestants, title="Meet the contestants")

@app.route('/add_contestant', methods=['GET', 'POST'])
def add_contestant():
    form = AddContestant()
    # Check if the form has been submitted (is a POST request) and form inputs are valid
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Create a Contestant object for saving to the database, mapping form inputs to object
        contestant = Contestant()
        form.populate_obj(obj=contestant)
        # Adds the contestant object to session for creation and saves changes to db
        db.session.add(contestant)
        db.session.commit()
        
        # Returns the view with a message that the contestant has been added
        # return render_template('add_contestant.html', contestant = contestant, title="Contestant Added")
        return redirect(url_for('contestants'))
    # When there is a GET request, the view with the form is returned
    return render_template('add_contestant.html', form = form)

@app.route('/edit_contestant', methods=['GET', 'POST'])
def edit_contestant():
    form = EditContestant()
    form.name.choices = get_current_contestants()
    # Check if the form has been submitted (is a POST request) and form inputs are valid
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Create a Contestant object for saving to the database, mapping form inputs to object
        contestant = Contestant()
        form.populate_obj(obj=contestant)
        # Adds the contestant object to session for creation and saves changes to db
        db.session.query.filter_by(contestant)
        db.session.commit()
        
        # Returns the view with a message that the contestant has been added
        # return render_template('add_contestant.html', contestant = contestant, title="Contestant Added")
        return redirect(url_for('contestants'))
    # When there is a GET request, the view with the form is returned
    return render_template('edit_contestant.html', form = form)

# Send user to the Tipping page - allows user to place a tip, then saves to the votes file
@app.route('/vote', methods = ['GET', 'POST'])
def vote():
    form = AddVoteForm()
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

# Send user to Sign-up / registration page
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html', title="Sign Up")

# Do Sign-up / registration form submit
@app.route('/signup-received', methods = ["POST"])
def submit_sign_up():
    new_user = {}
    if request.method == "POST":
        new_user['name'] = request.form.get('name')
        new_user['username'] = request.form.get('username')
        new_user['pword'] = request.form.get('pword')
        new_user['email'] = request.form.get('email')
        new_user['score'] = 0
        # Returns the view with a message that the user has been added
        return render_template('sign_up_received.html', new_user = new_user, title="Sign Up Successful")

# send user to the login page
@app.route('/login')
def login():
    return render_template('login.html', title="Log In")

# Do login page form submit
@app.route('/login-received', methods = ["POST"])
def check_login():
    if request.method == "POST":
        user_name = request.form.get('username')
        pword = request.form.get('pword')
        # Add verfication and if statement depending on results, dummy code assumes 
        comments = load_from_file('chat.csv')
        user = {'username': user_name}
        # Returns the view with a message that the user is now logged in
        return render_template('index.html', title=TITLE, user=user, comments=comments)