from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import InputRequired, Length, NumberRange

class AddContestantForm(FlaskForm):
    country = StringField('Country', default='Australia')
    season = IntegerField('Season', default=6)
    name = StringField('Contestant Name', validators=[InputRequired(), Length(min=1, max=80)])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=18, max=99, message="Contestants must be over 18")])
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

class AddTribalForm(FlaskForm):
    tribal_date = DateField('Tribal Date:', default=date.today(), validators = [InputRequired()])
    submit = SubmitField('Create Tribal')