from flask import Blueprint

bp = Blueprint('chart', __name__, template_folder='templates')

from app.chart import routes