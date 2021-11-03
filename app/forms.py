from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import InputRequired

class AddVoteForm(FlaskForm):
    tribal_id = SelectField('Tribal Date:', coerce=int, validators = [InputRequired()])
    first_choice_id = SelectField('First vote: Contestant name:', coerce=int, validators = [InputRequired()])
    second_choice_id = SelectField('Second vote: Contestant name:', coerce=int)
    third_choice_id = SelectField('Third vote: Contestant name:', coerce=int)
    submit = SubmitField('Place Vote')

