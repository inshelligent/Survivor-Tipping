from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import InputRequired

class AddVoteForm(FlaskForm):
    tribal_id = SelectField('Tribal Date:', coerce=int, validators = [InputRequired()])
    first_choice_id = SelectField('First vote:', coerce=int, description='Your first choice to go home', validators = [InputRequired()])
    second_choice_id = SelectField('Second vote:', coerce=int)
    third_choice_id = SelectField('Third vote:', coerce=int)
    submit = SubmitField('Place Vote')

