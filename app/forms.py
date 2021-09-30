from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length

class AddVoteForm(FlaskForm):
    voter_id = IntegerField('Voter ID:', validators = [InputRequired()])
    tribal_date = StringField('Tribal Date:', validators = [InputRequired()])
    first_vote = IntegerField('First vote: Contestant name:', validators = [InputRequired()])
    second_vote = IntegerField('Second vote: Contestant name:')
    third_vote = IntegerField('Third vote: Contestant name:')
    submit = SubmitField('Place Vote')

class AddContestant(FlaskForm):
    name = StringField('Contestant Name', validators=[InputRequired(), Length(min=1, max=80)])
    age = IntegerField('Age')
    occupation = StringField('Occupation')
    description = StringField('Description')
    is_eliminated = BooleanField('Is eliminated?')
    submit = SubmitField('Add Contestant')