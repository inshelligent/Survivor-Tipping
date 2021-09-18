from datetime import date
from app import app
from flask import Flask, render_template, request
import csv

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
def menu():
    players = load_from_file('competitors.csv')
    # Returns the view with list of contestants
    return render_template('contestants.html', players=players, title=TITLE)

# Send user to the Tipping page - allows user to place a tip, then saves to the votes file
@app.route('/bet', methods = ['GET', 'POST'])
def bet():
    # Check if the form has been submitted (is a POST request)
    if request.method == 'POST':
        # Get data from the form and put in dictionary
        vote = {}
        vote['voter'] = request.form.get('voter')
        vote['date'] = request.form.get('tribal_date')
        vote['name'] = request.form.get('contestant')
        # Load the votes from the CSV file and add the vote
        votes = load_from_file('votes.csv')
        votes.append(vote)
        # Open up the csv file and overwrite the contents
        with open('votes.csv', 'w', newline='') as file:
            fieldnames = ['voter', 'date', 'name']
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerows(votes)
        
        # Returns the view with a message that the student has been added
        return render_template('vote_successful.html', vote = vote, title=TITLE)

    else:
        user = {'username': 'Kylie'}  # hard-coded for now
        how_to='This is how to vote'
        contestants_left = ["Hayley", "George", "Wai", "Flick", "Cara"]  # hard-coded for now
        today = date.today()
        # Returns the view with a message of how to bet, and list of remaining contestants
        return render_template('bet.html', user=user, how_to=how_to, date=today, contestants_left=contestants_left, title=TITLE)

# Send user to Sign-up / registration page
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

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
        return render_template('sign_up_received.html', new_user = new_user, title=TITLE)

# send user to the login page
@app.route('/login')
def login():
    return render_template('login.html')

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