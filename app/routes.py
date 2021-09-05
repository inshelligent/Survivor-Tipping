import csv
from app import app
from flask import Flask, render_template, request
TITLE = "Cosy Couch Survivor"
def load_from_file(fname):
    # loads the contents from a given csv file
    contents = []
    with open(fname) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            contents.append(row)
    return contents

@app.route('/')
@app.route('/index')
def index():
    comments = load_from_file('chat.csv')
    user = {'username': 'Kylie'}
    return render_template('index.html', title=TITLE, user=user, comments=comments)

# adding new navigation links
@app.route('/orders')
def orders():
    return render_template('orders.html', title=TITLE)

@app.route('/contestants')
def menu():
    players = load_from_file('competitors.csv')
        
    return render_template('contestants.html', players=players, title=TITLE)

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
        user = {'username': 'Kylie'}
        how_to='This is how to bet'
        contestants_left = ["Hayley", "George", "Wai", "Flick", "Cara"]
        return render_template('bet.html', user=user, how_to=how_to, contestants_left=contestants_left, title=TITLE)

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/signup-received', methods = ["POST"])
def submit_sign_up():
    #print(request.form)
    #return ("Sign Up received")

    new_user = {}
    if request.method == "POST":
        new_user['name'] = request.form.get('name')
        new_user['pword'] = request.form.get('pword')
        new_user['domain'] = request.form.get('domain')

        return render_template('sign_up_received.html', new_user = new_user, title=TITLE)