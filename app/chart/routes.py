import json

from flask import render_template
from flask_login import login_required
import pandas as pd
import plotly.express as px
import plotly

from app import db
from app.chart import bp
from app.models import Contestant, User

@bp.route('/chart')
@login_required
def chart_list():
    return render_template('chart_list.html', title = 'Survivor Charts')

@bp.route('/user_scores')
@login_required
def user_scores_chart():
    # Retrieve all the users in the collection
    score_query = User.query
    df = pd.read_sql(score_query.statement, score_query.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x='username', y='score', 
    labels={'username': 'User', 'score': "Score"}
    , template='plotly_dark')
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Current User Scores', chart_JSON = chart_JSON)

@bp.route('/contestant_ages')
@login_required
def contestant_ages_chart():
    # Retrieve all the Contestants in the collection
    age_query = Contestant.query
    df = pd.read_sql(age_query.statement, age_query.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x='name', y='age', 
    labels={'name': 'Contestant', 'age': "Age"}
    , template='plotly_dark')
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Contestant Ages', chart_JSON = chart_JSON)

@bp.route('/contestant_votes')
@login_required
def contestant_votes_pie_chart():
# Run query to get count of votes of each user and load into DataFrame
    query = (
        "SELECT name, count(*) as vote_count FROM vote "
        "INNER JOIN contestant ON "
        "vote.first_choice_id = contestant.id "
        "GROUP BY name;"
    )
    df = pd.read_sql(query, db.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.pie(df, values ='vote_count', names='name',
    color='name', labels={'name': "Contestant", 'vote_count': 'Number of Votes'}
    , title='First Choice Votes by Contestant', template='plotly_dark')
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Votes by Contestant', chart_JSON = chart_JSON)

@bp.route('/votes_by_tribal')
@login_required
def votes_by_tribal_chart():
# Run query to get count of votes of each user and load into DataFrame
    query = (
        "SELECT name, tribal_id, first_choice_id FROM vote "
        "INNER JOIN contestant ON "
        "vote.first_choice_id = contestant.id "
        "ORDER BY tribal_id, name;"
    )
    df = pd.read_sql(query, db.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='name', y='first_choice_id',
    color='name', labels={'name': "Contestant", "first_choice_id": 'Votes'}
    , title='Contestant Votes by Tribal', template='plotly_dark', 
    barmode='group', facet_row="tribal_id")
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Contestant Votes by Tribal', chart_JSON = chart_JSON)