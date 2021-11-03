from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app import db
from app.auth import bp
from app.models import User
from .forms import LoginForm, AddUserForm


# Send user to Sign-up / registration page
@bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = AddUserForm()
    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid
        # Create a User object for saving to the database, mapping form inputs to object
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
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Find the user based off the name that has been entered in form
        user = User.query.filter_by(username=form.username.data).first()
        # Check if the user actually exists in the database
        if user is not None:
            # Check if the correct password has been entered and login, if so
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(url_for('index'))
        flash('Invalid username or password')

    # If there is a GET request, or there are errors in the form, return the view with the form
    return render_template('login.html', title = 'Login', form = form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
