from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, DateTimeField
from wtforms.validators import InputRequired, Length


class AddVoteForm(FlaskForm):
    #tribal_date = DateTimeField('Tribal Date:', format="%d-%m-%Y", default=date.today(), validators = [InputRequired()])
    tribal_id = IntegerField('Tribal No:', validators = [InputRequired()])
    first_choice_id = SelectField('First vote: Contestant name:', coerce=int, validators = [InputRequired()])
    second_choice_id = SelectField('Second vote: Contestant name:', coerce=int)
    third_choice_id = SelectField('Third vote: Contestant name:', coerce=int)
    submit = SubmitField('Place Vote')
    

class AddContestant(FlaskForm):
    name = StringField('Contestant Name', validators=[InputRequired(), Length(min=1, max=80)])
    age = IntegerField('Age')
    occupation = StringField('Occupation')
    description = StringField('Description')
    is_eliminated = BooleanField('Is eliminated?')
    submit = SubmitField('Add Contestant')