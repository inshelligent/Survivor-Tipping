from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, DateField, TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange

class AddContestantForm(FlaskForm):
    season_id = SelectField('Season', default='1')
    name = StringField('Contestant Name', validators=[InputRequired(), Length(min=1, max=80)])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=18, max=80, message="Contestants must be aged between 18 and 80")])
    occupation = StringField('Occupation', validators=[Length(max=80)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    is_eliminated = BooleanField('Is eliminated?', default=False)
    submit = SubmitField('Add Contestant')

class EditContestantForm(AddContestantForm):   # nice bit of inheritance happening here!
    submit = SubmitField('Save Contestant')

class EliminateContestantForm(FlaskForm):
    tribal_id = SelectField('Tribal:', coerce=int, validators = [InputRequired()])
    voted_out_id = SelectField('Contestant name:', coerce=int, validators = [InputRequired()])
    submit = SubmitField('Eliminate Contestant')

class AddTribalForm(FlaskForm):
    tribal_date = DateField('Tribal Date:', default=date.today(), validators = [InputRequired()])
    submit = SubmitField('Create Tribal')

class AddSeasonForm(FlaskForm):
    country = StringField('Country:', validators = [InputRequired()])
    season_number = IntegerField("Season number:", validators=[InputRequired(), NumberRange(min=1)])
    about = StringField("About:", validators=[InputRequired(), Length(min=10, max=250)])
    is_current = BooleanField('Set as current:')
    submit = SubmitField('Add Season')

class EditSeasonForm(AddSeasonForm):   # nice bit of inheritance happening here!
    submit = SubmitField('Save Season')