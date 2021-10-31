from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated == False:
            flash('You must be logged in to view this page.')
            return redirect(url_for('auth.login'))

        if current_user.is_admin == False:
            flash('That is an admin-only view! Not for you!')
            return redirect(url_for('index'))

        return f(*args, **kwargs)
    return decorated_function