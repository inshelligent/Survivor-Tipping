from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired

class AddVoteForm(FlaskForm):
    voter_id = StringField('Voter ID:', validators = [InputRequired()])
    tribal_date = StringField('Tibal Date:', validators = [InputRequired()])
    first_vote = IntegerField('First vote: Contestant name:', validators = [InputRequired()])
    second_vote = IntegerField('Second vote: Contestant name:')
    third_vote = IntegerField('Third vote: Contestant name:')
    submit = SubmitField('Place Vote')
