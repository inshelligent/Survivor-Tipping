from flask import render_template, redirect, url_for, flash
from sqlalchemy.sql.expression import null   # Flask is already imported in _init_
from flask_login import current_user

from app import db
from app.admin import bp
from app.models import Contestant, Tribal, Vote
from .forms import AddContestantForm, EditContestantForm, EliminateContestantForm, AddTribalForm
from app.auth.decorators import admin_required

TITLE = "Cosy Couch Survivor"

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

@bp.route('/admin_home')
@admin_required
def admin_home():
    return render_template('admin.html', title=TITLE)

@bp.route('/admin_contestants')
@admin_required
def admin_contestants():
    # The records from the table are retrieved and put in an iterable data structure
    contestants = Contestant.query.all()
    # Returns the view with list of contestants
    return render_template('admin_contestants.html', contestants=contestants, title="Contestant Admin")

@bp.route('/add_contestant', methods=['GET', 'POST'])
@admin_required
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
        return redirect(url_for('admin.admin_contestants'))
    # When there is a GET request, the view with the form is returned
    return render_template('add_contestant.html', form = form)

@bp.route('/edit_contestant/<int:id>', methods = ['GET', 'POST'])
@admin_required
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
        return redirect(url_for('admin.admin_contestants'))

    # When there is a GET request, the view with the form is returned
    contestant_name = f'{contestant.name}'
    return render_template('edit_contestant.html', form = form, contestant_name = contestant_name)

@bp.route('/delete_contestant/<int:id>')
@admin_required
def delete_contestant(id):
    # Retrieves the contestant record for the given id
    contestant = Contestant.query.get_or_404(id)
    # check that the contestant isn't part of a tribal or vote to maintain referential integrity
    check_tribals = Tribal.query.filter_by(voted_out_id=id).count()
    check_votes1 = Vote.query.filter_by(first_choice_id=id).count()
    check_votes2 = Vote.query.filter_by(second_choice_id=id).count()
    check_votes3 = Vote.query.filter_by(third_choice_id=id).count()
    if check_tribals + check_votes1 + check_votes2 + check_votes3 == 0:
        # The contestant record is deleted
        db.session.delete(contestant)
        # The change (the deletion) ie saved in the database file
        db.session.commit()
        flash('Contestant was deleted successfully!')
    else:
        flash('Contestant is in use and cannot be deleted!')
    
    # Returns the view that displays the list of contestants
    return redirect(url_for('admin.admin_contestants'))

@bp.route('/eliminate_contestant', methods=['GET', 'POST'])
@admin_required
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

        return redirect(url_for('admin.admin_contestants'))

    return render_template('eliminate_contestant.html', form = form)



# TRIBAL SECTION #
# Admin Tribal Page - allows an admin to create a tribal record
@bp.route('/add_tribal', methods = ['GET', 'POST'])
@admin_required
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
        return redirect(url_for('admin.admin_home'))
    # Returns the view with a message of how to bet, and list of remaining contestants
    return render_template('add_tribal.html', form = form, title="Create a Tribal")
