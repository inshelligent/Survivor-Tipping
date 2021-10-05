from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, HiddenField, PasswordField, DateField
from wtforms.validators import InputRequired, Length, EqualTo


class AddVoteForm(FlaskForm):
    tribal_id = SelectField('Tribal No:', coerce=int, validators = [InputRequired()])
    first_choice_id = SelectField('First vote: Contestant name:', coerce=int, validators = [InputRequired()])
    second_choice_id = SelectField('Second vote: Contestant name:', coerce=int)
    third_choice_id = SelectField('Third vote: Contestant name:', coerce=int)
    submit = SubmitField('Place Vote')

    # check all 3 votes are not the same  ## THIS DOES NOT WORK
"""    def validate(self):
        if not form.validate(self):
            return False
        result = True
        seen = set()
        for field in [self.first_choice_id, self.second_choice_id, self.third_choice_id]:
            if field.data in seen:
                field.errors.append('Please select three distinct choices.')
                result = False
            else:
                seen.add(field.data)
        return result  """
    

class AddContestantForm(FlaskForm):
    country = StringField('Country', default='Australia')
    season = IntegerField('Season', default=6)
    name = StringField('Contestant Name', validators=[InputRequired(), Length(min=1, max=80)])
    age = IntegerField('Age')
    occupation = StringField('Occupation')
    description = StringField('Description')
    is_eliminated = BooleanField('Is eliminated?', default=False)
    submit = SubmitField('Add Contestant')

class EditContestantForm(AddContestantForm):   # nice bit of inheritance happening here!
    submit = SubmitField('Save Contestant')

class EliminateContestantForm(FlaskForm):
    tribal_id = SelectField('Tribal:', coerce=int, validators = [InputRequired()])
    voted_out_id = SelectField('Contestant name:', coerce=int, validators = [InputRequired()])
    submit = SubmitField('Eliminate Contestant')

class AddUserForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired(), Length(min=1, max=50)])
    surname = StringField('Surname', validators=[InputRequired(), Length(min=1, max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    email = StringField('email', validators=[InputRequired(), Length(min=5, max=50)])
    submit = SubmitField('Register')
   
    # need to check if username already exists

class AddTribalForm(FlaskForm):
    tribal_date = DateField('Tribal Date:', default=date.today(), validators = [InputRequired()])
    submit = SubmitField('Create Tribal')