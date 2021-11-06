import json

from flask import render_template
from flask_login import login_required
import pandas as pd
import plotly.express as px
import plotly

from app import db
from app.chart import bp
from app.models import Contestant

@bp.route('/')
@login_required
def chart_list():
    return render_template('chart_list.html', title = 'Survivor Charts')

@bp.route('/contestant_ages')
@login_required
def contestant_ages_chart():
    # Retrieve all the books in the collection
    age_query = Contestant.query
    df = pd.read_sql(age_query.statement, age_query.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x='name', y='age', 
    labels={'name': 'Contestant', 'age': "Age"}
    , template='plotly_dark')
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Contestant Ages', chart_JSON = chart_JSON)
