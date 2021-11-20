from flask import render_template, redirect, url_for, flash
from sqlalchemy.sql.expression import null   # Flask is already imported in _init_
from flask_login import current_user

from app import db
from app.admin import bp
from app.models import Contestant, Season, Tribal, Vote, Season
from .forms import AddContestantForm, EditContestantForm, EliminateContestantForm, AddTribalForm, AddSeasonForm, EditSeasonForm
from app.auth.decorators import admin_required

TITLE = "Cosy Couch Survivor"
CURRENT_SEASON = 1

def get_current_contestants():
    # A helper function that returns a list of tuples with contestant ids and names from the contestants table.
    # This is used to populate the choices in the Contestants for each voting choice dropdown.
    contestants = [(player.id, player.name) for player in Contestant.query.filter_by(season_id=CURRENT_SEASON ,is_eliminated=False)]
    return contestants

def get_current_tribals():
    # A helper function that returns a list of tuples with tribal ids and dates from the tribals table.
    # This is used to populate the choices for the tribal choice dropdown, in the Vote form and on the Eliminate Contestant admin page
    # thanks to stackoverflow for how to format the date :)
    tribals = [(tribal.id, tribal.tribal_date.strftime("%a %d %b %Y")) for tribal in Tribal.query.filter_by(voted_out_id=0)]
    return tribals

def get_seasons():
    # A helper function that returns a list of tuples with tribal ids and dates from the tribals table.
    # This is used to populate the choices for the tribal choice dropdown, in the Vote form and on the Eliminate Contestant admin page
    seasons = [(season.id, season.country + " season " + str(season.season_number)) for season in Season.query.all()]
    return seasons

@bp.route('/admin_home')
@admin_required
def admin_home():
    return render_template('admin.html', title=TITLE)


# CONTESTANTS SECTION 
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
    form.season_id.choices = get_seasons()
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

    # set all the counts back to zero
    check_tribals = check_votes1 = check_votes2 = check_votes3 = 0
    
    # Returns the view that displays the list of contestants
    return redirect(url_for('admin.admin_contestants'))

@bp.route('/eliminate_contestant', methods=['GET', 'POST'])
@admin_required
def eliminate_contestant():
    ''' Based on the results of a tribal council 
    set a contestant;s eliminated state to True and update 
    user scores based on this information'''
    form = EliminateContestantForm()
    # Load dropdowns for the current Tribals and contestants
    form.tribal_id.choices = get_current_tribals()
    form.voted_out_id.choices = get_current_contestants()

    if form.validate_on_submit():
        
        tribalTemp = Tribal()
        form.populate_obj(obj=tribalTemp)
        # get the eliminated contestant info and update the is_eliminated field
        contestant = Contestant.query.get_or_404(tribalTemp.voted_out_id)
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
        # get the votes for tribal and update the user scores
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
        flash('New tribal was added successfully!')
        # Returns the view with a message that the student has been added
        return redirect(url_for('admin.admin_home'))
    # Returns the view with a message of how to bet, and list of remaining contestants
    return render_template('add_tribal.html', form = form, title="Create a Tribal")


# SEASON SECTION #
# Admin Manage Seasons Pages - allows an admin to add, edit or delete season record

@bp.route('/admin_seasons')
@admin_required
def admin_seasons():
    seasons = Season.query.all()
    # Returns the view with list of seasons
    return render_template('admin_seasons.html', seasons=seasons, title="Season Admin")

@bp.route('/add_season', methods = ['GET', 'POST'])
@admin_required
def add_season():
    form = AddSeasonForm()
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Get data from the form and put in a Season object
        season = Season()
        form.populate_obj(obj=season)
        # Adds the season object to session for creation and saves changes to db
        if Season.query.filter_by(is_current=True).count() == 0:
            db.session.add(season)
            db.session.commit()
            flash('New season was added successfully!')
        else:
            flash("Season already is progress! Only one season can be set to current at a time.")
        # Returns the view with a message
        return redirect(url_for('admin.admin_home'))
    # Returns the view with a message of how to bet, and list of remaining contestants
    return render_template('add_season.html', form = form, title="Create a new season of Survivor")

@bp.route('/edit_season/<int:id>', methods = ['GET', 'POST'])
@admin_required
def edit_season(id):
    # Retrieves the season record for the given id, if it exists
    season = Season.query.get_or_404(id)
    # Creates a form for editing the season record
    form = EditSeasonForm(obj=season)
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Create a Season object for saving to the database, mapping form inputs to object
        form.populate_obj(season)
        db.session.commit()
        flash('Season details were saved successfully!')
        return redirect(url_for('admin.admin_seasons'))

    # When there is a GET request, the view with the form is returned
    season_details = f'Season {season.season_number} of Survivor {season.country}'
    return render_template('edit_season.html', form = form, season_details = season_details)

@bp.route('/delete_season/<int:id>')
@admin_required
def delete_season(id):
    # Retrieves the contestant record for the given id
    season = Season.query.get_or_404(id)
    # check that the season doesn't has any contestants associated
    check_contestants = Contestant.query.filter_by(season_id=id).count()
    if check_contestants == 0:
        # The season record is deleted
        db.session.delete(season)
        db.session.commit()
        flash('Season was deleted successfully!')
    else:
        flash('Season is in use and cannot be deleted!')
    
    # Returns the view that displays the list of contestants
    return redirect(url_for('admin.admin_seasons'))