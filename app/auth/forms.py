from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Length, EqualTo, Email, DataRequired
from wtforms.fields.html5 import EmailField

class AddUserForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired(), Length(min=1, max=50)])
    surname = StringField('Surname', validators=[InputRequired(), Length(min=1, max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    email = EmailField("Email",  validators=[InputRequired("Please enter your email address."), Email("Please enter your email address.")])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('Old Password', validators=[InputRequired(), Length(min=8, max=20)])
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=20), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Change Password')